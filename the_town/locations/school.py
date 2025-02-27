from relative_world_ollama.tools import tool
from the_town.events import JobInquiryEvent, SchoolEvent
from the_town.locations.tooledlocation import TooledLocation

class School(TooledLocation):
    """A school."""
    name: str = "The School"
    description: str = "A place for education and learning. Available subjects: Math, Science, History, Art."
    subjects: list[str] = ["Math", "Science", "History", "Art"]

    @tool
    def attend_class(self, actor, subject: str):
        if subject in self.subjects:
            actor.emit_event(SchoolEvent(actor=actor, location=self.id, subject=subject))
            print(f"📚 {actor.name} is attending a {subject} class at {self.name}")
            return f"Attending a {subject} class at the school"
        else:
            print(f"❌ {subject} is not available at the school")
            return f"{subject} is not available at the school"

    @tool
    def inquire_about_job(self, actor):
        actor.emit_event(JobInquiryEvent(actor=actor, location=self.id))
        print(f"💼 {actor.name} is inquiring about a job at {self.name}")
        return f"Inquiring about a job at {self.name}"