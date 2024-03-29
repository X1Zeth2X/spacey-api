from uuid import uuid4
from flask import current_app
from sqlalchemy.sql.expression import func

from api.util import Message, InternalErrResp, ErrResp

from api.main.model.fact import Fact

from .utils import (
    add_fact_and_flush,
    delete_fact,
    load_fact,
    update_fact,
    facts_schema,
    solar_planets,
)


class FactService:
    @staticmethod
    def create(data, current_user):
        # Assign the vars
        content = data["content"]
        planet = data["planet"]

        # Set limits
        content_limit = 500
        title_limit = 50

        if data["title"] is not None:
            title = data["title"]

            # Validate title
            if len(title) > title_limit:
                return ErrResp(
                    f"Given data exceeds limits (Title: {title_limit}, Content: {content_limit})",
                    "exceeded_limits",
                    400,
                )
        else:
            title = None

        # Check if the content doesn't exceed limits
        if not content:
            return ErrResp("Required items are empty", "data_404", 400)

        # Make sure content and title don't exceed their limits
        elif len(content) > content_limit:
            return ErrResp(
                f"Given data exceeds limits (Title: {title_limit}, Content: {content_limit})",
                "exceeded_limits",
                400,
            )

        if planet.title() not in solar_planets:
            return ErrResp(
                f"The planet specified is not in the solar system!\
                  If it is just a general knowledge fact, use 'unspecified'",
                "planet_unknown",
                400,
            )

        try:
            public_id = str(uuid4())[:15]
            new_fact = Fact(
                public_id=public_id,
                author_id=current_user.id,
                planet=planet.title(),
                title=title,
                content=content,
            )

            latest_fact = add_fact_and_flush(new_fact)

            resp = Message(True, "Fact added.")
            resp["fact"] = latest_fact
            return resp, 201

        except Exception as error:
            current_app.logger.error(error)
            return InternalErrResp()

    @staticmethod
    def delete(fact_public_id, current_user):
        fact = Fact.query.filter_by(public_id=fact_public_id).first()

        if not fact:
            return ErrResp("Fact not found!", "fact_404", 404)

        # Check fact owner
        elif current_user.id == fact.author_id:
            try:
                delete_fact(fact)

                resp = Message(True, "Fact has been deleted.")
                return resp, 200

            except Exception as error:
                current_app.logger.error(error)
                return InternalErrResp()

        return ErrResp("Insufficient permissions!", "insufficient_permission", 403)

    @staticmethod
    def get(fact_public_id):
        fact = Fact.query.filter_by(public_id=fact_public_id).first()

        if not fact:
            return ErrResp("Fact not found!", "fact_404", 404)

        fact_info = load_fact(fact)

        resp = Message(True, "Fact data sent.")
        resp["fact"] = fact_info
        return resp, 200

    @staticmethod
    def update(fact_public_id, data, current_user):
        fact = Fact.query.filter_by(public_id=fact_public_id).first()

        if not fact:
            return ErrResp("Fact not found!", "fact_404", 404)

        # Check owner
        elif current_user.id == fact.author_id:
            if not data["content"]:
                return ErrResp("Update content not found!", "content_404", 400)

            try:
                update_fact(fact, data["content"])

                resp = Message(True, "Fact content updated.")
                return resp, 200

            except Exception as error:
                current_app.logger.error(error)
                return InternalErrResp()

        return ErrResp("Insufficient permissions!", "insufficient_permissions", 403)


class FactsFeedService:
    @staticmethod
    def get(limit):
        if limit > 100:
            return ErrResp("You have exceeded the limit (100)", "limits_exceeded", 400)

        # Get random facts based on limits
        random_facts = Fact.query.order_by(func.random()).limit(limit)

        # Load their info
        random_facts_info = facts_schema.dump(random_facts)

        resp = Message(True, "Random facts sent!")
        resp["facts"] = random_facts_info
        return resp, 200

    @staticmethod
    def get_by_planet(planet_name, limit):
        if limit > 100:
            return ErrResp("You have exceeded the limit (100)", "limits_exceeded", 400)

        # Get random facts that belongs to that planet
        if planet_name not in solar_planets:
            return ErrResp("Planet not found!", "planet_404", 404,)

        planet_random_facts = (
            Fact.query.filter_by(planet=planet_name).order_by(func.random()).limit(10)
        )

        # Load their info
        planet_random_facts_info = facts_schema.dump(planet_random_facts)

        resp = Message(True, "Planet's random facts sent.")
        resp["facts"] = planet_random_facts_info
        return resp, 200
