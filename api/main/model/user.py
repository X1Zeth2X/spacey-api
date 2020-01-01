from datetime import datetime

from api.main import db, ma, bcrypt

# Alias common SQLAlchemy names
Column = db.Column
Model = db.Model
relationship = db.relationship

roles_users = db.Table(
    "roles_users",
    Column("user_id", db.Integer, db.ForeignKey("user.id")),
    Column("role_id", db.Integer, db.ForeignKey("role.id")),
)


class User(Model):

    # Basic details
    id = Column(db.Integer, primary_key=True)
    email = Column(db.String(255), unique=True)
    username = Column(db.String(15), unique=True)
    full_name = Column(db.String(50))
    password_hash = Column(db.String(255))

    # Statuses
    joined_date = Column(db.DateTime, default=datetime.utcnow)

    facts_created = relationship("Fact", backref="author", lazy=True)

    @property
    def password(self):
        raise AttributeError("Password: Write-Only field")

    @password.setter
    def password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode("utf-8")

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<User '{ self.username }'>"


class Role(Model):
    """ Role Model for storing role related details """

    __tablename__ = "role"

    id = Column(db.Integer, primary_key=True)
    name = Column(db.String(20), unique=True)
    description = Column(db.String(50))

    def __repr__(self):
        return f"<{ self.name } - { self.description }>"
