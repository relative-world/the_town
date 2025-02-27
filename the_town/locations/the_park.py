from relative_world_ollama.tools import tool

from the_town.locations.tooledlocation import TooledLocation
from the_town.events import ParkActivityEvent, JobInquiryEvent


class Park(TooledLocation):
    """A park."""
    name: str = "The Park"
    description: str = "A place to relax and enjoy nature."

    @tool
    def sit_on_bench(self, actor):
        actor.emit_event(ParkActivityEvent(actor=actor, location=self.id, activity="sitting on bench"))
        print(f"🪑 {actor.name} is sitting on a bench in the park")
        return "Sitting on a bench in the park"

    @tool
    def play_with_dog(self, actor):
        actor.emit_event(ParkActivityEvent(actor=actor, location=self.id, activity="playing with dog"))
        print(f"🐶 {actor.name} is playing with a dog in the park")
        return "Playing with a dog in the park"

    @tool
    def inquire_about_job(self, actor):
        actor.emit_event(JobInquiryEvent(actor=actor, location=self.id))
        print(f"💼 {actor.name} is inquiring about a job at {self.name}")
        return f"Inquiring about a job at {self.name}"
