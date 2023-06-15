from flask_security import RoleMixin

from app.core.database.database import db
from app.models.data.base_model import BaseModel


class Role(RoleMixin, BaseModel):
    __tablename__ = "role"
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    description = db.Column(db.String(255), nullable=True)
    permissions = db.Column(db.UnicodeText)
