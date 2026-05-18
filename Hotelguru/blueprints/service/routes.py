from Hotelguru.blueprints.service import bp
from Hotelguru.blueprints.service.schemas import ServiceResponseSchema
from Hotelguru.blueprints.service.service import ServiceService
from apiflask import HTTPError


@bp.get('/hotel/<int:hotelid>')
@bp.doc(tags=["service"])
@bp.output(ServiceResponseSchema(many=True))
def get_services_by_hotel(hotelid):
    success, response = ServiceService.get_services_by_hotel(hotelid)
    if success:
        return response, 200
    return {"message": response}, 400
