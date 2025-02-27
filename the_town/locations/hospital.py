from relative_world_ollama.tools import tool
from the_town.events import JobInquiryEvent, MedicalEvent
from the_town.locations.tooledlocation import TooledLocation

class Hospital(TooledLocation):
    """A hospital."""
    name: str = "The Hospital"
    description: str = "A place to receive medical care."
    services: list[str] = ["Checkup", "Emergency", "Surgery"]

    @tool
    def receive_treatment(self, actor, service: str):
        if service in self.services:
            actor.emit_event(MedicalEvent(actor=actor, location=self.id, service=service))
            print(f"🏥 {actor.name} is receiving {service} at {self.name}")
            return f"Receiving {service} at the hospital"
        else:
            print(f"❌ {service} is not available at the hospital")
            return f"{service} is not available at the hospital"

    @tool
    def inquire_about_job(self, actor):
        actor.emit_event(JobInquiryEvent(actor=actor, location=self.id))
        print(f"💼 {actor.name} is inquiring about a job at {self.name}")
        return f"Inquiring about a job at {self.name}"
