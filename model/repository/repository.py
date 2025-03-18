from sqlalchemy.orm import sessionmaker
from model.models import Base
from sqlalchemy import create_engine

engine = create_engine('sqlite:///travel_agency.db', echo=True)
Session = sessionmaker(bind=engine)
session = Session()

def init_db():
    Base.metadata.create_all(engine)

    #for documentation i need all the attributes and methods of the view class, if they are privete they should start like : - _name and form methods like : - get_name() if they are public they should start like: + name and form methods like: + get_name()
    #Attributes:
    