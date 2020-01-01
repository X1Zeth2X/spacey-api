from api.util import Message, InternalErrResp, ErrResp

from api.main.model.fact import Fact

class FactService:
    @staticmethod
    def create(data, current_user):
        # Assign the vars
        title = data["title"]
        content = data["content"]

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
            new_fact = Fact(
            )