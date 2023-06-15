from app.core.database.database import db
from app.models.data.base_model import BaseModel


class Plugin(BaseModel):
    __tablename__ = "plugin"
    name = db.Column(db.String(250), unique=True, nullable=False)
    kwargs = db.Column(db.Text, unique=True, nullable=True, default={})
    enabled = db.Column(db.Boolean, default=False)

    def __repr__(self) -> str:
        return f"<Plugin {self.name}>"
