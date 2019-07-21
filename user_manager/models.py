import datetime

from sqlalchemy import (
    Column,
    DateTime,
    Integer,
    Float,
    MetaData,
    String,
    ForeignKey,
    Table,
    Boolean,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


class Base(object):
    created_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime,
        default=datetime.datetime.utcnow,
        onupdate=datetime.datetime.utcnow,
        nullable=False,
    )


DeclarativeBase = declarative_base(cls=Base, metadata=MetaData(schema="user_manager"))


group_user_table = Table(
    "group_user",
    DeclarativeBase.metadata,
    Column("group_id", Integer, ForeignKey("groups.id")),
    Column("user_id", Integer, ForeignKey("users.id")),
)


class User(DeclarativeBase):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    expiration_date = Column(DateTime, nullable=False)
    is_activated = Column(Boolean, default=True, nullable=False)
    groups = relationship("Group", secondary=group_user_table, back_populates="users")
    profile_pictures = relationship("ProfilePicture", back_populates="user")

    def as_dict(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "expiration_date": self.expiration_date.isoformat(),
            "is_activated": self.is_activated,
            "profile_pictures": [
                {"id": profile_picture.id, "link": profile_picture.picture_url}
                for profile_picture in self.profile_pictures
            ],
            "groups": [{"id": group.id, "name": group.name} for group in self.groups],
        }


class ProfilePicture(DeclarativeBase):
    __tablename__ = "profile_pictures"

    id = Column(Integer, primary_key=True, autoincrement=True)
    picture_url = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    user = relationship("User", back_populates="profile_pictures")


group_area_table = Table(
    "group_area",
    DeclarativeBase.metadata,
    Column("group_id", Integer, ForeignKey("groups.id")),
    Column("area_id", Integer, ForeignKey("areas.id")),
)


class Group(DeclarativeBase):
    __tablename__ = "groups"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    areas = relationship("Area", secondary=group_area_table, back_populates="groups")
    users = relationship("User", secondary=group_user_table, back_populates="groups")

    def as_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "users": [
                {
                    "id": user.id,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                }
                for user in self.users
            ],
            "areas": [{"id": area.id, "name": area.name} for area in self.areas],
        }


class Area(DeclarativeBase):
    __tablename__ = "areas"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    groups = relationship("Group", secondary=group_area_table, back_populates="areas")
