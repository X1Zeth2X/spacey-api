from datetime import datetime

from api.main import db

# Alias common SQLAlchemy names
Column = db.Column
Model = db.Model
relationship = db.relationship


class Fact(Model):
    """ Fact model for storing fact related stuff *shrug* """

    # Basic details
    id = Column(db.Integer, primary_key=True)
    public_id = Column(db.String(15))
    author_id = Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    planet = Column(db.String(15))

    # Fact content
    title = Column(db.String(50), nullable=True)
    content = Column(db.Text)

    created_at = Column(db.DateTime, default=datetime.utcnow)
    updated_at = Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Fact '{self.public_id}'>"
