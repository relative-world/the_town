from relative_world.location import Location
from relative_world_ollama.entity import TooledMixin


class TooledLocation(TooledMixin, Location):
    description: str

    def llm_describe(self):
        return f"""
        location name: {self.name} 
        location description: {self.description}.
        location details: {self.details}.        
        """

    @property
    def details(self):
        return "No details provided."
