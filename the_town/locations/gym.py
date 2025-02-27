from relative_world_ollama.tools import tool

from the_town.events import GymClassEvent, UseEquipmentEvent, JobInquiryEvent
from the_town.locations.tooledlocation import TooledLocation


class Gym(TooledLocation):
    """A gym."""
    name: str = "The Gym"
    description: str = "A place to work out and get fit."
    equipment: list[str] = ["treadmill", "weights", "yoga mat"]
    classes: list[str] = ["yoga", "spin", "zumba"]

    @tool
    def take_class(self, actor):
        actor.emit_event(GymClassEvent(actor=actor, location=self.id))
        print(f"🏋️ {actor.name} is taking a class at {self.name}")
        return "Taking a class in the gym"

    @tool
    def use_equipment(self, actor):
        actor.emit_event(UseEquipmentEvent(actor=actor, location=self.id))
        print(f"💪 {actor.name} is using equipment at {self.name}")
        return "Using equipment in the gym"

    @tool
    def inquire_about_job(self, actor):
        actor.emit_event(JobInquiryEvent(actor=actor, location=self.id))
        print(f"💼 {actor.name} is inquiring about a job at {self.name}")
        return f"Inquiring about a job in {self.name}"
