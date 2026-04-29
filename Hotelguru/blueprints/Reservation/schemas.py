from apiflask import Schema
from apiflask.fields import (
 Integer,
 String,
 DateTime,
 List
)

from marshmallow import validates_schema
from marshmallow import ValidationError


class ReservationCreateSchema(
    Schema
):

    user_id=Integer(required=True)

    reserved_start_date=DateTime(
       required=True
    )

    reserved_end_date=DateTime(
       required=True
    )

    room_ids=List(
        Integer(),
        required=True
    )


    @validates_schema
    def validate_dates(
        self,
        data,
        **kwargs
    ):

        if (
            data["reserved_end_date"]
            <=
            data["reserved_start_date"]
        ):
            raise ValidationError(
               "Invalid date range"
            )


class ReservationResponseSchema(
    Schema
):
    id=Integer()
    status=String()
    user_id=Integer()