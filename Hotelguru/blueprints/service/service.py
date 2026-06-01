from Hotelguru.models.Service import Service
from Hotelguru.models.Hotel import Hotel
from Hotelguru.models.ReservationService import ReservationService
from Hotelguru.extensions import db
from Hotelguru.blueprints.service.schemas import ServiceResponseSchema
from sqlalchemy import select


class ServiceService:

    @staticmethod
    def get_services_by_hotel(hotelid):
        services = db.session.execute(
            db.select(Service).filter_by(hotel_id=hotelid)
        ).scalars().all()
        return True, ServiceResponseSchema().dump(services, many=True)

    @staticmethod
    def add_service(data):
        try:
            hotel = db.session.get(Hotel, data["hotel_id"])
            if not hotel:
                return False, "Hotel not found"
            service = Service(
                name=data["name"],
                price=data["price"],
                hotel_id=data["hotel_id"],
            )
            db.session.add(service)
            db.session.commit()
            return True, ServiceResponseSchema().dump(service)
        except Exception as ex:
            db.session.rollback()
            return False, str(ex)

    @staticmethod
    def update_service(service_id, data):
        try:
            service = db.session.get(Service, service_id)
            if not service:
                return False, "Service not found"
            if "name" in data:
                service.name = data["name"]
            if "price" in data:
                service.price = data["price"]
            db.session.commit()
            return True, ServiceResponseSchema().dump(service)
        except Exception as ex:
            db.session.rollback()
            return False, str(ex)

    @staticmethod
    def delete_service(service_id):
        try:
            service = db.session.get(Service, service_id)
            if not service:
                return False, "Service not found"
            in_use = db.session.execute(
                select(ReservationService.id).filter_by(service_id=service_id)
            ).first()
            if in_use:
                return False, "Service is linked to reservations and cannot be deleted"
            db.session.delete(service)
            db.session.commit()
            return True, {"message": "Service deleted"}
        except Exception as ex:
            db.session.rollback()
            return False, str(ex)
