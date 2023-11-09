from flask_security import RoleMixin

from app.core.database.database import db
from app.models.data.base_model import BaseModel


class Database(BaseModel):
  __tablename__ = "database"
  name = db.Column(db.String(255), unique=True)
  database_type = db.Column(db.String(255), unique=False, nullable=False)
  description = db.Column(db.String(255), nullable=True)
  database_uri = db.Column(db.Text, unique=False, nullable=False)

  def __repr__(self) -> str:
    return f"<Database {self.name}, {self.database_type}, {self.database_uri}>"
