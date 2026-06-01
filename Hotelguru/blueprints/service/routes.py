from Hotelguru.blueprints.service import bp
from Hotelguru.blueprints.service.schemas import (
    ServiceResponseSchema,
    ServiceRequestSchema,
    ServiceUpdateSchema,
)
from Hotelguru.blueprints.service.service import ServiceService
from Hotelguru.extensions import auth
from Hotelguru.blueprints import role_required


@bp.get('/services/<int:hotelid>')
@bp.doc(tags=["service"])
@bp.output(ServiceResponseSchema(many=True))
def get_services_by_hotel(hotelid):
    success, response = ServiceService.get_services_by_hotel(hotelid)
    if success:
        return response, 200
    return {"message": response}, 400


@bp.post('/services')
@bp.doc(tags=["service"])
@bp.input(ServiceRequestSchema, location="json")
@bp.output(ServiceResponseSchema)
@bp.auth_required(auth)
@role_required(["Adminisztrátor"])
def add_service(json_data):
    success, response = ServiceService.add_service(json_data)
    if success:
        return response, 200
    return {"message": response}, 400


@bp.put('/services/<int:service_id>')
@bp.doc(tags=["service"])
@bp.input(ServiceUpdateSchema, location="json")
@bp.output(ServiceResponseSchema)
@bp.auth_required(auth)
@role_required(["Adminisztrátor"])
def update_service(service_id, json_data):
    success, response = ServiceService.update_service(service_id, json_data)
    if success:
        return response, 200
    return {"message": response}, 400


@bp.delete('/services/<int:service_id>')
@bp.doc(tags=["service"])
@bp.auth_required(auth)
@role_required(["Adminisztrátor"])
def delete_service(service_id):
    success, response = ServiceService.delete_service(service_id)
    if success:
        return response, 200
    return {"message": response}, 400
