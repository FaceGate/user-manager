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


class ProfilePicture(DeclarativeBase):
    __tablename__ = "profile_pictures"

    id = Column(Integer, primary_key=True, autoincrement=True)
    picture_url = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)


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


class Area(DeclarativeBase):
    __tablename__ = "areas"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    groups = relationship("Group", secondary=group_area_table, back_populates="areas")
