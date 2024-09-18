from flask import jsonify
from sqlalchemy import Column, String
from sqlalchemy.dialects.mysql import CHAR
from database import Base, SessionLocal
import uuid
import re


class Client(Base):
    __tablename__ = 'clients'

    id = Column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()), unique=True, index=True)
    name = Column(String(255), index=True)
    email = Column(String(255), unique=True, index=True)
    phone = Column(String(20))


def create_client(name: str, email: str, phone: str):
    session = SessionLocal()
    new_client = Client(name=name, email=email, phone=phone)
    session.add(new_client)
    session.commit()
    session.refresh(new_client)
    session.close()
    return new_client
