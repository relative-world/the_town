import uuid

from relative_world.actor import Actor
from relative_world.event import Event


class OrderCoffeeEvent(Event):
    type: str = "ORDER_COFFEE"
    actor: Actor
    location: uuid.UUID
    coffee_type: str


class ReadMenuEvent(Event):
    type: str = "READ_MENU"
    actor: Actor
    location: uuid.UUID


class JobInquiryEvent(Event):
    type: str = "JOB_INQUIRY"
    actor: Actor
    location: uuid.UUID
    vacancy: bool = False


class GymClassEvent(Event):
    type: str = "GYM_CLASS"
    actor: Actor
    location: uuid.UUID


class UseEquipmentEvent(Event):
    type: str = "USE_EQUIPMENT"
    actor: Actor
    location: uuid.UUID


class ReadBookEvent(Event):
    type: str = "READ_BOOK"
    actor: Actor
    location: uuid.UUID
    book: str


class BrowseBooksEvent(Event):
    type: str = "BROWSE_BOOKS"
    actor: Actor
    location: uuid.UUID


class ParkActivityEvent(Event):
    type: str = "PARK_ACTIVITY"
    actor: Actor
    location: uuid.UUID
    activity: str


class StatementEvent(Event):
    type: str = "STATEMENT"
    speaker: str
    statement: str


class MoveEvent(Event):
    type: str = "MOVE"
    actor: Actor
    from_location: uuid.UUID
    to_location: uuid.UUID


class MedicalEvent(Event):
    type: str = "MEDICAL"
    actor: Actor
    location: uuid.UUID
    service: str


class SchoolEvent(Event):
    type: str = "SCHOOL"
    actor: Actor
    location: uuid.UUID
    subject: str


class TheaterEvent(Event):
    type: str = "THEATER"
    actor: Actor
    location: uuid.UUID
    show: str
