import uuid
from collections import Counter
from typing import Annotated

from pydantic import PrivateAttr, computed_field
from relative_world.actor import Actor
from relative_world.event import Event
from relative_world.location import Location
from relative_world_ollama.entity import TooledMixin, OllamaEntity
from relative_world_ollama.responses import BasicResponse
from relative_world_ollama.tools import wrap_with_actor, tools_to_schema, tool

from the_town.events import MoveEvent, StatementEvent


def render_events(event_buffer):
    output = []
    for event in event_buffer:
        if isinstance(event, MoveEvent):
            output.append(f"{event.actor.name} moved from {event.from_location} to {event.to_location}")
        if isinstance(event, StatementEvent):
            output.append(f"{event.speaker}: {event.statement}")
        else:
            output.append(f"{event}")
    return "\n".join(output)


class TooledActor(Actor, TooledMixin, OllamaEntity):
    description: str
    private_knowledge: str
    _recent_events: Annotated[list[Event], PrivateAttr()] = []
    _event_buffer: Annotated[list[Event], PrivateAttr()] = []
    _location_tools: Annotated[dict[str, str], PrivateAttr()] = {}
    _gained_attributes: Annotated[Counter, PrivateAttr(default_factory=Counter)]

    def get_system_prompt(self):
        connected_locations = ", ".join(
            [
                f"{loc.name} (id={loc.id})" for loc in self.world.get_connected_locations(self.location.id)
            ]
        )
        location_children = self.world.get_location(self.location.id).children
        if len(location_children) > 1:
            other_actors = ", ".join([
                f"{actor.name} ({actor.description})" for actor in filter(
                    lambda x: isinstance(x, Actor), self.world.get_location(self.location.id).children
                )
            ])
            other_actor_statement = f"Other actors in location: {other_actors}."
        else:
            other_actor_statement = "You are alone here."

        return (f"You are {self.name}. "
                f"Your character description: {self.description}. "
                f"Information about your current location: {self.location.llm_describe()}. "
                f"Connected locations: {connected_locations}. "
                f"{other_actor_statement} ",
                f"These are your highest ranked gained attributes: {self._gained_attributes.most_common(3)}. "
                f"Your private knowledge: {self.private_knowledge}. "
                )

    def get_prompt(self):
        event_buffer, self._events = self._event_buffer, []

        recent_events = render_events(event_buffer)
        if not recent_events:
            recent_events = "No events yet. do anything you'd like, this is the beginning of the journey."

        return f"""{recent_events}"""

    async def handle_event(self, entity, event: Event):
        if entity is self:
            attribute_gain = None
            if event.type == "STATEMENT":
                print(f"🗣️ ({self.location.name}) {event.speaker} said: \"{event.statement}\"")
                attribute_gain = "talkative"
            if event.type == "MOVE":
                attribute_gain = "adventurous"
            if event.type == "GYM_CLASS":
                attribute_gain = "fit"
            if event.type == "USE_EQUIPMENT":
                attribute_gain = "fit"
            if event.type == "READ_BOOK":
                attribute_gain = "knowledgeable"
            if event.type == "BROWSE_BOOKS":
                attribute_gain = "knowledgeable"
            if event.type == "PARK_ACTIVITY":
                attribute_gain = "relaxed"
            if event.type == "JOB_INQUIRY":
                attribute_gain = "ambitious"
            if attribute_gain:
                self._gained_attributes[attribute_gain] += 1
        self._event_buffer.append(event)

    def render_recent_events(self):
        return render_events(self._recent_events)

    async def generate_response(self, prompt, system, response_model):
        tools = dict(self._tools)
        tools.update(self._location_tools)

        return await self.ollama_client.generate(
            prompt=prompt,
            system=system,
            response_model=response_model,
            context=self._context,
            tools=tools,
        )

    async def handle_response(self, response: BasicResponse) -> None:
        if not response:
            return
        self.emit_event(StatementEvent(speaker=self.name, statement=response.text))

    @computed_field
    @property
    def location(self) -> Location | None:
        """
        Gets the location of the actor within the world.

        Returns
        -------
        Location | None
            The location of the actor.
        """
        if not self.location_id:
            return None
        if world := self.world:
            return world.get_location(self.location_id)
        return None

    @location.setter
    def location(self, value):
        """
        Sets the location of the actor within the world.

        Parameters
        ----------
        value : Location
            The new location for the actor.
        """
        if self.location:
            self.location.remove_entity(self)
        self.location_id = value.id
        value.add_entity(self)

        location_tools = {}
        for key, value in self.location.__class__.__dict__.items():
            if callable(value) and hasattr(value, "_is_tool"):
                location_tools[key] = wrap_with_actor(getattr(self.location, key), actor=self)
        self._location_tools = tools_to_schema(location_tools)

    @tool
    def move(self, location_id: str):
        location = self.world.get_location(uuid.UUID(location_id))
        if location:
            print(f"🔄 {self.name} moved to {location.name}")
            self.emit_event(
                MoveEvent(
                    actor=self,
                    from_location=self.location.id,
                    to_location=location_id)
            )
            self.location = location
            return True
        else:
            print(f"❌ {self.name} failed to move to \"{location_id}\"")
            return False
