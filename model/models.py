from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import declarative_base
import datetime

Base = declarative_base()

class Package(Base):      
    __tablename__ = 'packages'
    id = Column(Integer, primary_key=True, autoincrement=True)
    price = Column(Float, nullable=False)
    destination = Column(String, nullable=False)
    period = Column(Integer, nullable=False)
    image_1 = Column(String)
    image_2 = Column(String)
    image_3 = Column(String)

class Client(Base):
    __tablename__ = 'clients'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    phone = Column(String, nullable=False)

class BoughtPackage(Base):
    __tablename__ = 'bought_packages'
    id = Column(Integer, primary_key=True, autoincrement=True)
    package_id = Column(Integer, ForeignKey('packages.id'))
    client_id = Column(Integer, ForeignKey('clients.id'))
    bought_date = Column(String, nullable=False)
    departure = Column(String, nullable=False)
    arrival = Column(String, nullable=False)
