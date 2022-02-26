from datetime import datetime

from disckeep.web import db
from sqlalchemy.ext.declarative import DeclarativeMeta

BaseModel: DeclarativeMeta = db.Model


class Group(BaseModel):
    id = db.Column(db.String(length=36), primary_key=True)
    name = db.Column(db.String(64), index=True)
    follow = db.Column(db.Boolean(), default=False)
    last_updated = db.Column(db.DateTime(), default=datetime.utcnow)

    def __repr__(self):
        return f"<group {self.name}>"


class ReleaseGroup(BaseModel):
    id = db.Column(db.String(length=36), primary_key=True)
    name = db.Column(db.String(64), index=True)
    release_type_primary = db.Column(db.String(64))
    # TODO: Move this to its own table since a release group can have multiplesecondary types.
    release_types_secondary = db.Column(db.String(64))
    release_date = db.Column(db.DateTime())
    group_id = db.Column(db.String(length=36), db.ForeignKey("group.id"))
    # 0 = Not listened
    # 1 = Want to listen
    # 2 = Don't want to listen
    # 3 = Already listened
    listen_status = db.Column(db.Integer, default=0)
    # 0 = Neutral
    # 1 = Interested
    # 2 = Not interested
    # 3 = Owned
    want_status = db.Column(db.Integer, default=0)

    def __repr__(self):
        return f"<release {self.name}>"


class ReleaseGroupType(BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)
    primary = db.Column(db.Boolean(), default=False)
    track = db.Column(db.Boolean(), default=False)

    def __repr__(self):
        return f"<release_type {self.name}>"
