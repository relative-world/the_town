import json
import random

from relative_world.world import RelativeWorld
from the_town.actors import TooledActor
from the_town.locations.cafe import Cafe
from the_town.locations.docks import Docks
from the_town.locations.gym import Gym
from the_town.locations.hospital import Hospital
from the_town.locations.library import Library
from the_town.locations.mall import Mall
from the_town.locations.police_station import PoliceStation
from the_town.locations.school import School
from the_town.locations.the_park import Park
from the_town.locations.theater import Theater


async def main():
    with open('the_town/assets/json/the_town.json', 'r') as f:
        setup = json.load(f)

    world = RelativeWorld()

    location_classes = {
        "Gym": Gym,
        "Library": Library,
        "Park": Park,
        "Hospital": Hospital,
        "Cafe": Cafe,
        "Docks": Docks,
        "Mall": Mall,
        "Theater": Theater,
        "School": School,
        "Police Station": PoliceStation,
    }

    locations = {}
    for loc in setup["locations"]:
        location = location_classes[loc["type"]]()
        locations[loc["name"]] = location
        world.add_location(location)

    for loc_a, loc_b in setup["connections"]:
        world.connect_locations(locations[loc_a].id, locations[loc_b].id)

    _actors = setup["actors"][::]
    random.shuffle(_actors)
    for actor_data in _actors:
        actor = TooledActor(
            name=actor_data["name"],
            description=actor_data["description"],
            private_knowledge=actor_data["private_knowledge"]
        )
        actor.world = world
        actor.location = locations[actor_data["location"]]

    for _ in range(10):
        await world.step()

if __name__ == "__main__":

    import asyncio

    asyncio.run(main())
