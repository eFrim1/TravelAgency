from ..models import BoughtPackage
from ..models import Client
from .repository import Session
import datetime

class BoughtPackageRepository:
    @staticmethod
    def get_all():
        session = Session()
        try:
            return session.query(BoughtPackage).all()
        finally:
            session.close()

    @staticmethod
    def get_by_id(bought_id):
        session = Session()
        try:
            return session.query(BoughtPackage).filter_by(id=bought_id).first()
        finally:
            session.close()

    @staticmethod
    def add(bought_package_data):
        session = Session()
        try:
            bought_package = BoughtPackage()
            bought_package.package_id = int(bought_package_data.package_id.strip())
            bought_package.client_id = int(bought_package_data.client_id.strip())
            bought_package.bought_date = datetime.datetime.strptime(bought_package_data.bought_date.strip(), "%d-%m-%Y")
            bought_package.departure = datetime.datetime.strptime(bought_package_data.bought_date.strip(), "%d-%m-%Y")
            bought_package.arrival = datetime.datetime.strptime(bought_package_data.bought_date.strip(), "%d-%m-%Y")
            session.add(bought_package)
            session.commit()
            return bought_package
        except Exception as e:
            session.rollback()
            print(f"Error adding bought package: {e}")
            return None
        finally:
            session.close()

    @staticmethod
    def delete(bought_id):
        session = Session()
        try:
            bought_package = session.query(BoughtPackage).filter_by(id=bought_id).first()
            if bought_package:
                session.delete(bought_package)
                session.commit()
                return True
            return False
        except Exception as e:
            session.rollback()
            print(f"Error deleting bought package: {e}")
            return False
        finally:
            session.close()
    
    @staticmethod
    def update(bought_package_data):
        session = Session()
        try:
            existing_bought_package = session.query(BoughtPackage).filter_by(id=bought_package_data.id).first()
            if existing_bought_package:
                existing_bought_package.package_id = int(bought_package_data.package_id.strip())
                existing_bought_package.bought_date = datetime.datetime.strptime(bought_package_data.bought_date.strip(), "%Y-%m-%d")
                existing_bought_package.departure = datetime.datetime.strptime(bought_package_data.bought_date.strip(), "%d-%m-%Y")
                existing_bought_package.arrival = datetime.datetime.strptime(bought_package_data.bought_date.strip(), "%d-%m-%Y")
                session.commit()
                return True
            return False
        except Exception as e:
            session.rollback()
            print(f"Error updating bought package: {e}")
            return False
        finally:
            session.close()
    
    @staticmethod
    def get_by_client_name(client_name : str):
        session = Session()
        try:
            if client_name == "":
                return session.query(BoughtPackage).all()
            return session.query(BoughtPackage).join(Client).filter(Client.name == client_name).all()
        finally:
            session.close()

    #for documentation i need all the attributes and methods of the view class, if they are privete they should start like : - _name and form methods like : - get_name() if they are public they should start like: + name and form methods like: + get_name()
    #Attributes:
    # + _session : Session
    #Methods:
    # + __init__(self)
    # + get_all(self) -> List[BoughtPackage]
    # + get_by_id(self, bought_id : int) -> BoughtPackage
    # + add(self, bought_package_data : BoughtPackage) -> BoughtPackage
    # + delete(self, bought_id : int) -> bool
    # + update(self, bought_package_data : BoughtPackage) -> bool
    # + get_by_client_name(self, client_name : str) -> List[BoughtPackage]