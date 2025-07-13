from typing import Any, Dict

from sqlalchemy import select, Column, Integer
from sqlalchemy.orm import declared_attr
from sqlmodel import SQLModel
from sqlalchemy_continuum import make_versioned, versioning_manager
from sqlalchemy_continuum.plugins import (
    ActivityPlugin,
    FlaskPlugin,
    PropertyModTrackerPlugin,
)

from models.users import Users

# ---- configure SQLAlchemy-Continuum -------------------------------------- #
_activity_plugin = ActivityPlugin()


class VersionedBase:
    """Mixin that adds Continuum helpers to a model."""

    __versioned__: Dict[str, Any] = {}  # marker required by Continuum
    __allow_unmapped__ = True

    # ← THIS IS THE KEY: inject an `id` Column into every Version class
    @declared_attr
    def id(cls) -> Column:
        return Column(
            Integer,
            nullable=False,
            index=True,
            # Not primary_key=True, because Continuum uses (id, transaction_id) as the composite PK
        )

    class Config:
        table = False  # ← don't create a DB table for this mixin itself

    # ---- convenience helpers -------------------------------------------- #
    def get_versions(self, session):
        return self.versions.all()

    def revert_to_version(self, session, version_id: int):
        version = session.get(self.__class__.versions_class, version_id)
        for attr, value in vars(version).items():
            if attr not in {
                "id",
                "_sa_instance_state",
                "transaction_id",
                "end_transaction_id",
            }:
                setattr(self, attr, value)
        session.commit()

    # ---- class-level queries -------------------------------------------- #
    @classmethod
    def get_transaction_log(cls, session):
        txn_cls = versioning_manager.transaction_cls
        return session.scalars(select(txn_cls)).all()

    @classmethod
    def get_activities(cls, session):
        activity_cls = _activity_plugin.activity_cls
        return session.scalars(select(activity_cls)).all()


# Configure SQLAlchemy-Continuum
versioning_manager.plugins.append(_activity_plugin)
versioning_manager.plugins.append(FlaskPlugin())
versioning_manager.plugins.append(PropertyModTrackerPlugin())

make_versioned(
    user_cls=Users,
    plugins=[_activity_plugin, FlaskPlugin()],
    options={
        "base_classes": (VersionedBase,),
    },
)
