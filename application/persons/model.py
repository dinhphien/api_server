from flask_restx import fields

person_model ={
    "entityID": fields.String(required=True, description="The unique identifier of a Person"),
    "name": fields.String(required=True, description="Person name"),
    "des": fields.String(required=True, description="Person description"),
}
entity_with_type_model = {
    "set_entity_id": fields.List(fields.String, required=True, description="A list contains a set of"
                                                                         "entities identified by their id"),
}
