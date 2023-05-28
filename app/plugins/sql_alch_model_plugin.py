from app import db


class Plugin(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(250), unique=True, nullable=False)
  kwargs = db.Column(db.Text, unique=True, nullable=False)
  enabled = db.Column(db.Boolean, default=False)

  def __repr__(self) -> str:
    return f'<Plugin {self.name}>'
