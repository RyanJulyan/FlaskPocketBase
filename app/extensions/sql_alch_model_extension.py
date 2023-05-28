from app import db


class Extension(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(50), unique=True, nullable=False)
  enabled = db.Column(db.Boolean, default=False)

  def __repr__(self):
    return f'<Extension {self.name}>'
