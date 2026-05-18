from Hotelguru.models.Service import Service
from Hotelguru.extensions import db
from Hotelguru.blueprints.service.schemas import ServiceResponseSchema

class ServiceService:

    @staticmethod
    def get_services_by_hotel(hotelid):
        services = db.session.execute(db.select(Service).filter_by(hotel_id=hotelid)).scalars().all()
        return True, ServiceResponseSchema().dump(services, many=True)
