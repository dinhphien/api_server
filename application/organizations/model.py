from flask_restx import fields

organization_model ={
    "entityID": fields.String(required=True, description="The unique identifier of an Organization"),
    "name": fields.String(required=True, description="Organization name"),
    "des": fields.String(required=True, description="Organization description"),
}
entity_with_type_model = {
    "set_entity_id": fields.List(fields.String, required=True, description="A list contains a set of"
                                                                         "entities identified by their id"),
}