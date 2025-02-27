from relative_world_ollama.tools import tool
from the_town.events import JobInquiryEvent
from the_town.locations.tooledlocation import TooledLocation

class Mall(TooledLocation):
    """A mall."""
    name: str = "The Mall"
    description: str = ("A place to shop and socialize. "
                        "Available stores include Clothing Store, Electronics Store, "
                        "Food Court, and Fashion Store.")
    stores: list[str] = ["Clothing Store", "Electronics Store", "Food Court", "Fashion Store"]

    @tool
    def visit_store(self, actor, store: str):
        if store in self.stores:
            print(f"🛍️ {actor.name} is visiting the {store} at {self.name}")
            return f"Visiting the {store} in the mall"
        else:
            print(f"❌ {store} is not available in the mall")
            return f"{store} is not available in the mall"

    @tool
    def inquire_about_job(self, actor):
        actor.emit_event(JobInquiryEvent(actor=actor, location=self.id))
        print(f"💼 {actor.name} is inquiring about a job at {self.name}")
        return f"Inquiring about a job at {self.name}"
