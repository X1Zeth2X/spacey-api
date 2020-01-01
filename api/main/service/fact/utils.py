# Fact service utils
from datetime import datetime
from api.main import db

# Import Schemas
from api.main.model.schemas import FactSchema

# Define deserializers
fact_schema = FactSchema()

# Define solar system's planets
solar_planets = (
    "Mercury",
    "Venus",
    "Earth",
    "Mars",
    "Jupiter",
    "Saturn",
    "Uranus",
    "Neptune",
    "Pluto",
)
# "I know that, Pluto is no longer considered a planet,
# it's a dwarf planet but it is also still a planet
# in our solar system."


def update_fact(fact, content):
    fact.title = title
    fact.content = content

    fact.updated_at = datetime.utcnow()

    db.session.commit()


def delete_fact(fact):
    db.session.delete(fact)
    db.session.commit()


def add_fact_and_flush(data):
    db.session.add(data)
    db.session.flush()

    latest_fact = load_fact(data)

    db.session.commit()

    return latest_fact


def load_fact(fact):
    info = fact_schema.dump(fact)

    # Add other stuff here later

    return info
