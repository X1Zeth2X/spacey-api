from uuid import uuid4
from flask import current_app

from api.util import Message, InternalErrResp, ErrResp

from api.main.model.fact import Fact

from .utils import add_fact_and_flush, delete_fact, load_fact, update_fact


class FactService:
    @staticmethod
    def create(data, current_user):
        # Assign the vars
        title = data["title"]
        content = data["content"]
        planet = data["content"]

        # Set limits
        content_limit = 500
        title_limit = 50

        # Check if the content doesn't exceed limits
        if not content or not title:
            ErrResp("Required items are empty", "data_404", 400)

        # Make sure content and title don't exceed their limits
        elif len(content) > content_limit or len(title) > title_limit:
            ErrResp(
                f"Given data exceeds limits (Title: {title_limit}, Content: {content_limit})",
                "exceeded_limits",
                400,
            )

        try:
            public_id = str(uuid4())[:15]
            new_fact = Fact(
                public_id=public_id,
                author_id=current_user.id,
                planet=planet,
                title=title,
                content=content,
            )

            latest_fact = add_fact_and_flush(new_fact)

            resp = Message(True, "Fact added.")
            resp["fact"] = latest_fact
            return resp, 201

        except Exception as error:
            current_app.logger.error(error)
            InternalErrResp()

    @staticmethod
    def delete(fact_public_id, current_user):
        fact = Fact.query.filter_by(public_id=fact_public_id).first()

        if not fact:
            ErrResp("Fact not found!", "fact_404", 404)

        # Check fact owner
        elif current_user.id == fact.author_id:
            try:
                delete_fact(fact)

                resp = Message(True, "Fact has been deleted.")
                return resp, 200

            except Exception as error:
                current_app.logger.error(error)
                InternalErrResp()

        ErrResp("Insufficient permissions!", "insufficient_permission", 403)

    @staticmethod
    def get(fact_public_id):
        fact = Fact.query.filter_by(public_id=fact_public_id).first()

        if not fact:
            ErrResp("Fact not found!", "fact_404", 404)

        fact_info = load_fact(fact)

        resp = Message(True, "Fact data sent.")
        resp["fact"] = fact_info
        return resp, 200

    @staticmethod
    def update(fact_public_id, data, current_user):
        fact = Fact.query.filter_by(public_id=fact_public_id).first()

        if not fact:
            ErrResp("Fact not found!", "fact_404", 404)

        # Check owner
        elif current_user.id == fact.author_id:
            if not data["content"]:
                ErrResp("Update content not found!", "content_404", 400)

            try:
                update_fact(fact, data["content"])

                resp = Message(True, "Fact content updated.")
                return resp, 200

            except Exception as error:
                current_app.logger.error(error)
                InternalErrResp()

        ErrResp("Insufficient permissions!", "insufficient_permissions", 403)
