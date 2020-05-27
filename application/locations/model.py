from flask_restx import fields

location_model ={
    "entityID": fields.String(required=True, description="The unique identifier of a Location"),
    "name": fields.String(required=True, description="Location name"),
    "des": fields.String(required=True, description="Location description"),
}

entity_with_type_model = {
    "set_entity_id": fields.List(fields.String, required=True, description="A list contains a set of"
                                                                         "entities identified by their id"),
}