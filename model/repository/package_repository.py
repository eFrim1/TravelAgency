from models import Package
from .repository import Session

class PackageRepository:
    @staticmethod
    def get_all():
        session = Session()
        try:
            return session.query(Package).all()
        finally:
            session.close()

    @staticmethod
    def get_by_id(package_id):
        session = Session()
        try:
            return session.query(Package).filter_by(id=package_id).first()
        finally:
            session.close()

    @staticmethod
    def add(package_data):
        session = Session()
        try:
            package = Package()
            package.price = float(package_data.price.strip())
            package.destination = package_data.destination.strip()
            package.period = int(package_data.period.strip())
            package.image_1 = package_data.image_1.strip()
            package.image_2 = package_data.image_2.strip()
            package.image_3 = package_data.image_3.strip()
            session.add(package)
            session.commit()
            return package
        except Exception as e:
            session.rollback()
            print(f"Error adding package: {e}")
            return None
        finally:
            session.close()

    @staticmethod
    def delete(package_id):
        session = Session()
        try:
            package = session.query(Package).filter_by(id=package_id).first()
            if package:
                session.delete(package)
                session.commit()
                return True
            return False
        except Exception as e:
            session.rollback()
            print(f"Error deleting package: {e}")
            return False
        finally:
            session.close()
    
    @staticmethod
    def update(package_data):
        session = Session()
        try:
            package = session.query(Package).filter_by(id=package_data.id).first()
            if package:
                package.price = float(package_data.price.strip())
                package.destination = package_data.destination.strip()
                package.period = int(package_data.period.strip())
                package.image_1 = package_data.image_1.strip()
                package.image_2 = package_data.image_2.strip()
                package.image_3 = package_data.image_3.strip()
                session.commit()
                return True
            return False
        except Exception as e:
            session.rollback()
            print(f"Error updating package: {e}")
            return False
        finally:
            session.close()
    
    @staticmethod
    def filter(filter_str, filter_type, compare_type="equal"):
        session = Session()
        try:
            if filter_str == "":
                return session.query(Package).all()
            elif filter_type == "price":
                if compare_type == "less":
                    return session.query(Package).filter(Package.price < float(filter_str)).all()
                elif compare_type == "equal":
                    return session.query(Package).filter(Package.price == float(filter_str)).all()
                elif compare_type == "greater":
                    return session.query(Package).filter(Package.price > float(filter_str)).all()
            elif filter_type == "destination":
                return session.query(Package).filter(Package.destination == filter_str).all()
            elif filter_type == "period":
                print(filter_str)
                if compare_type == "less":
                    return session.query(Package).filter(Package.period < float(filter_str)).all()
                elif compare_type == "equal":
                    return session.query(Package).filter(Package.period == float(filter_str)).all()
                elif compare_type == "greater":
                    return session.query(Package).filter(Package.period > float(filter_str)).all()
            else:
                return []
        finally:
            session.close()

    @staticmethod
    def sort(sort_type):
        session = Session()
        try:
            if sort_type == "price":
                return session.query(Package).order_by(Package.price).all()
            elif sort_type == "destination":
                return session.query(Package).order_by(Package.destination).all()
            elif sort_type == "period":
                return session.query(Package).order_by(Package.period).all()
            else:
                return []
        finally:
            session.close()


        #for documentation i need all the attributes and methods of the view class, if they are privete they should start like : - _name and form methods like : - get_name() if they are public they should start like: + name and form methods like: + get_name()
    #Attributes:
    #Methods:
    # + get_all() : List[Package]
    # + get_by_id(package_id : int) : Package
    # + add(package_data : Package) : Package
    # + delete(package_id : int) : bool
    # + update(package_data : Package) : bool
    # + filter(filter_str : str, filter_type : str, compare_type : str) : List[Package]
    # + sort(sort_type : str) : List[Package]