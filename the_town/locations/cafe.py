from relative_world_ollama.tools import tool
from the_town.events import OrderCoffeeEvent, ReadMenuEvent, JobInquiryEvent
from the_town.locations.tooledlocation import TooledLocation

class Cafe(TooledLocation):
    """A cafe."""
    name: str = "The Cafe"
    description: str = "A place to enjoy coffee and relax."
    menu: list[str] = ["Espresso", "Latte", "Cappuccino", "Americano"]

    @tool
    def order_coffee(self, actor, coffee_type: str):
        if coffee_type in self.menu:
            actor.emit_event(OrderCoffeeEvent(actor=actor, location=self.id, coffee_type=coffee_type))
            print(f"☕ {actor.name} ordered a {coffee_type} at {self.name}")
            return f"Ordered a {coffee_type} in the cafe"
        else:
            print(f"❌ {coffee_type} is not available in the menu")
            return f"{coffee_type} is not available in the menu"

    @tool
    def read_menu(self, actor):
        actor.emit_event(ReadMenuEvent(actor=actor, location=self.id))
        print(f"📜 {actor.name} is reading the menu at {self.name}")
        return self.menu

    @tool
    def inquire_about_job(self, actor):
        actor.emit_event(JobInquiryEvent(actor=actor, location=self.id))
        print(f"💼 {actor.name} is inquiring about a job at {self.name}")
        return f"Inquiring about a job at {self.name}"
