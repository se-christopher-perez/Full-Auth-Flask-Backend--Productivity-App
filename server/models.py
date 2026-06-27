from marshmallow import Schema, fields
from sqlalchemy.ext.hybrid import hybrid_property

from config import db, bcrypt

class User(db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True)
    _password_hash = db.Column(db.String)

    journal_entries = db.relationship("JournalEntry", back_populates="user")

    @hybrid_property
    def password_hash(self):
        raise AttributeError("Password hashes may not be viewed.")
    
    @password_hash.setter
    def password_hash(self, password):
        password_hash = bcrypt.generate_password_hash(password.encode("utf-8"))
        self._password_hash = password_hash.decode("utf-8")

    def authenticate(self, password):
        return bcrypt.check_password_hash(self._password_hash, password.encode("utf-8"))
    

class JournalEntry(db.Model):

    __tablename__ = "journal_entries"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    content = db.Column(db.String)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    user = db.relationship("User", back_populates="journal_entries")

class UserSchema(Schema):

    id = fields.Int()
    username = fields.String()

    journal_entries = fields.List(fields.Nested(lambda: JournalEntrySchema(exclude=("user",))))

class JournalEntrySchema(Schema):

    id = fields.Int()
    title = fields.String()
    content = fields.String()

    user = fields.Nested(UserSchema(exclude=("journal_entries",)))
