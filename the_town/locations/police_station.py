from relative_world_ollama.tools import tool
from the_town.events import JobInquiryEvent, StatementEvent
from the_town.locations.tooledlocation import TooledLocation

class PoliceStation(TooledLocation):
    """A police station."""
    name: str = "The Police Station"
    description: str = "A place where law enforcement officers work. "
    services: list[str] = ["File Report", "Request Assistance", "Inquire About Case"]

    @tool
    def file_report(self, actor, report: str):
        actor.emit_event(StatementEvent(speaker=actor.name, statement=report))
        print(f"📝 {actor.name} is filing a report at {self.name}")
        return f"Filing a report at the police station: {report}"

    @tool
    def request_assistance(self, actor, assistance: str):
        actor.emit_event(StatementEvent(speaker=actor.name, statement=assistance))
        print(f"🚓 {actor.name} is requesting assistance at {self.name}")
        return f"Requesting assistance at the police station: {assistance}"

    @tool
    def inquire_about_case(self, actor, case_id: str):
        actor.emit_event(StatementEvent(speaker=actor.name, statement=f"Inquiring about case {case_id}"))
        print(f"🔍 {actor.name} is inquiring about case {case_id} at {self.name}")
        return f"Inquiring about case {case_id} at the police station"

    @tool
    def inquire_about_job(self, actor):
        actor.emit_event(JobInquiryEvent(actor=actor, location=self.id))
        print(f"💼 {actor.name} is inquiring about a job at {self.name}")
        return f"Inquiring about a job at {self.name}"

