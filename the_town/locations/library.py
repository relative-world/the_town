from relative_world_ollama.tools import tool

from the_town.events import BrowseBooksEvent, ReadBookEvent, JobInquiryEvent
from the_town.locations.tooledlocation import TooledLocation


class Library(TooledLocation):
    """A library."""
    name: str = "The Library"
    books: list[str] = ["The Great Gatsby", "To Kill a Mockingbird", "1984"]
    description: str = "A place to read and study."

    @tool
    def get_books(self, actor):
        actor.emit_event(BrowseBooksEvent(actor=actor, location=self.id))
        print(f"📚 {actor.name} is browsing books at {self.name}")
        return self.books

    @tool
    def read_book(self, actor, book):
        actor.emit_event(ReadBookEvent(actor=actor, location=self.id, book=book))
        print(f"📚 {actor.name} is reading at {self.name}")
        return "Reading a book in the library"

    @tool
    def inquire_about_job(self, actor):
        actor.emit_event(JobInquiryEvent(actor=actor, location=self.id))
        print(f"💼 {actor.name} is inquiring about a job at {self.name}")
        return f"Inquiring about a job at {self.name}"
