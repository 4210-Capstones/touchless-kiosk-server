"""
Define database interactions here. Each database class shall have its own Service class inheriting from main service.
"""

from abc import ABC
from typing import Iterable

from sqlalchemy.orm import Session

from backend.classes.db_classes import DBParentClass, User
from backend.database.config_db import autocommit


class Service(ABC):
    """
    Parent database service class.
    Each database class shall have its own Service class inheriting from main service.

    This defines some operations which are expected to be equal among all classes.

    Usage:

    class CustomService(Service):
        model_class: [database class]

        ... # extend or overwrite Service functions

        # functions which write or delete from db should be decorated with @autocommit
    """
    model_class: DBParentClass

    @classmethod
    def get(cls, id: int, db: Session):
        result = db.query(cls.model_class).filter(cls.model_class.id == id).first()

        return result

    @classmethod
    def get_all(cls, db: Session, limit: int = 100):
       return db.query(cls.model_class).order_by(cls.model_class.id.asc()).limit(limit).all()

    @classmethod
    @autocommit
    def create(cls, t: DBParentClass, db: Session):
        db.add(t)
        return t

    @classmethod
    @autocommit
    def create_multiple(cls, ts: Iterable[DBParentClass], db: Session):
        for t in ts:
            db.add(t)

    @classmethod
    @autocommit
    def update(cls, id: int, t: DBParentClass, db: Session):
        t.id = id
        db.merge(t)
        return t

    @classmethod
    @autocommit
    def delete(cls, id: int, db: Session):
        obj = db.query(cls.model_class).filter(cls.model_class.id == id).one()
        db.delete(obj)
        return id


class UserService(Service):
    model_class = User
    
    @classmethod
    def get_by_mail(cls, mail: str, db: Session):
        return db.query(cls.model_class).filter(cls.model_class.user_email == mail).first()