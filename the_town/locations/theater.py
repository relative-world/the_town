from relative_world_ollama.tools import tool
from the_town.events import JobInquiryEvent, TheaterEvent
from the_town.locations.tooledlocation import TooledLocation

class Theater(TooledLocation):
    """A theater."""
    name: str = "The Theater"
    description: str = "A place to watch plays and performances. Available shows: Hamlet, Les Misérables, The Phantom of the Opera."
    shows: list[str] = ["Hamlet", "Les Misérables", "The Phantom of the Opera"]

    @tool
    def watch_show(self, actor, show: str):
        if show in self.shows:
            actor.emit_event(TheaterEvent(actor=actor, location=self.id, show=show))
            print(f"🎭 {actor.name} is watching {show} at {self.name}")
            return f"Watching {show} at the theater"
        else:
            print(f"❌ {show} is not available at the theater")
            return f"{show} is not available at the theater"

    @tool
    def inquire_about_job(self, actor):
        actor.emit_event(JobInquiryEvent(actor=actor, location=self.id))
        print(f"💼 {actor.name} is inquiring about a job at {self.name}")
        return f"Inquiring about a job at {self.name}"