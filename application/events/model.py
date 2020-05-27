from flask_restx import fields

event_model ={
    "entityID": fields.String(required=True, description="The unique identifier of an Event"),
    "name": fields.String(required=True, description="Event name"),
    "des": fields.String(required=True, description="Event description"),
}
entity_with_type_model = {
    "set_entity_id": fields.List(fields.String, required=True, description="A list contains a set of"
                                                                         "entities identified by their id"),
}
