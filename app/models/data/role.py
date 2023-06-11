from flask_security import RoleMixin

from app.core.database.database import db


class Role(RoleMixin, db.Model):
    __tablename__ = "role"
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(255), unique=True)
    description = db.Column(db.String(255))
    permissions = db.Column(db.UnicodeText)
