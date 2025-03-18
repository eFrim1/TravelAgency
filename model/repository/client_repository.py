from ..models import Client
from .repository import Session

class ClientRepository:
    @staticmethod
    def get_all():
        session = Session()
        try:
            return session.query(Client).all()
        finally:
            session.close()

    @staticmethod
    def get_by_id(client_id):
        session = Session()
        try:
            return session.query(Client).filter_by(id=client_id).first()
        finally:
            session.close()

    @staticmethod
    def add(client_data):
        session = Session()
        try:
            client = Client()
            client.name = client_data.name.strip()
            client.email = client_data.email.strip()
            client.phone = client_data.phone.strip()
            session.add(client)
            session.commit()
            return client
        except Exception as e:
            session.rollback()
            print(f"Error adding client: {e}")
            return None
        finally:
            session.close()

    @staticmethod
    def delete(client_id):
        session = Session()
        try:
            client = session.query(Client).filter_by(id=client_id).first()
            if client:
                session.delete(client)
                session.commit()
                return True
            return False
        except Exception as e:
            session.rollback()
            print(f"Error deleting client: {e}")
            return False
        finally:
            session.close()

    @staticmethod
    def update(client_data):
        session = Session()
        try:
            existing_client = session.query(Client).filter_by(id=client_data.id).first()
            if existing_client:
                existing_client.name = client_data.name.strip()
                existing_client.email = client_data.email.strip()
                existing_client.phone = client_data.phone.strip()
                session.commit()
                return True
            return False
        except Exception as e:
            session.rollback()
            print(f"Error updating client: {e}")
            return False
        finally:
            session.close()
    
        #for documentation i need all the attributes and methods of the view class, if they are privete they should start like : - _name and form methods like : - get_name() if they are public they should start like: + name and form methods like: + get_name()
    #Attributes:
    #Methods:
    # + get_all() : List[Client]
    # + get_by_id(client_id : int) : Client
    # + add(client_data : Client) : Client
    # + delete(client_id : int) : bool
    # + update(client_data : Client) : bool