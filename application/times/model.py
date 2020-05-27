from flask_restx import fields

time_model ={
    "entityID": fields.String(required=True, description="The unique identifier of a Time"),
    "name": fields.String(required=True, description="Time in String format"),
    "des": fields.Date(required=True, description="Time description in Date format"),
}
entity_with_type_model = {
    "set_entity_id": fields.List(fields.String, required=True, description="A list contains a set of"
                                                                         "entities identified by their id"),
}