from flask_security import RoleMixin

from app.core.database.database import db
from app.models.data.base_model import BaseModel


class Database(BaseModel):
    __tablename__ = "database"
    name = db.Column(db.String(255), unique=True)
    description = db.Column(db.String(255), nullable=True)
    kwargs = db.Column(db.Text, unique=True, nullable=False)

    def __repr__(self) -> str:
        return f"<Database {self.name}>"
