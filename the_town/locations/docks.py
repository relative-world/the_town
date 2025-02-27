from relative_world_ollama.tools import tool
from the_town.events import JobInquiryEvent, ParkActivityEvent
from the_town.locations.tooledlocation import TooledLocation

class Docks(TooledLocation):
    """A docks."""
    name: str = "The Docks"
    description: str = ("A place where ships dock and sailors gather. "
                        "Available activities are: \"fishing\", \"loading cargo\" and \"unloading cargo\".")
    activities: list[str] = ["fishing", "loading cargo", "unloading cargo"]

    @tool
    def perform_activity(self, actor, activity: str):
        if activity.strip().lower() in self.activities:
            actor.emit_event(ParkActivityEvent(actor=actor, location=self.id, activity=activity))
            print(f"⚓ {actor.name} is performing {activity} at {self.name}")
            return f"Performing {activity} at the docks"
        else:
            print(f"❌ {activity} is not available at the docks")
            return f"{activity} is not available at the docks"

    @tool
    def inquire_about_job(self, actor):
        actor.emit_event(JobInquiryEvent(actor=actor, location=self.id))
        print(f"💼 {actor.name} is inquiring about a job at {self.name}")
        return f"Inquiring about a job at {self.name}"