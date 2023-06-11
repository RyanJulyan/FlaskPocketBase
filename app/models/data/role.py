from flask import current_app as ca

from flask_security import RoleMixin


class Role(RoleMixin, ca.db.Model):
    id = ca.db.Column(ca.db.Integer(), primary_key=True)
    name = ca.db.Column(ca.db.String(255), unique=True)
