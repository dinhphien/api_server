from flask_restx import fields

URL_PATTERN = "http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+"
ENTITY_TYPES = ["Person","Country", "Location", "Time", "Event", "Organization", "Agreement"]
SUBJECT_TYPES = ["Person", "Country", "Organization"]
OBJECT_TYPES = ["Person", "Country", "Organization", "Event", "Agreement"]
RELATIONS = ["gặp gỡ", "tổ chức", "ký thỏa thuận", "tham gia", "ủng hộ", "phản đối", "phát biểu tại",
             "căng thẳng với", "hủy bỏ", "đàm phán với"]
LOCATION_TYPES = ["Location", "Country"]

news_model ={
    "entityID": fields.String(required=True, description="The unique identifier of a news"),
    "link": fields.String(required=True, description="URL news", pattern= URL_PATTERN),
    "topics": fields.List(fields.String, required=True, description="Specific areas that news refers such as:"
                                                       "Politics, Education, Sports, Heath,..."),
}

set_news_model = {
    "set_news_id": fields.List(fields.String, required=True, description= "A list contains a set of"
                                                                       "news identified by their id")
}

types_entity_model = {
    "set_entity_types": fields.List(fields.String(enum=ENTITY_TYPES),
                                  required=True, description="A list contains a set of types supported")
}

types_entity_set_news_model = {
    "set_entity_types": fields.List(fields.String(enum=ENTITY_TYPES),
                                  required=True, description="A list contains a set of types supported"),

    "set_news_id": fields.List(fields.String, required=True, description="A list contains a set of"
                                                                         "news identified by their id")
}

entity_with_type_model = {
    "set_entity_id": fields.List(fields.String, required=True, description="A list contains a set of"
                                                                         "entities identified by their id"),
    "entity_type": fields.String(required=True, description="The type of the entities", enum=ENTITY_TYPES)
}

fact_model = {
    "entityID": fields.String(required=True, description="Id of the fact"),
    "relation": fields.String(required=True, description="Relations between entities that are supported", enum=RELATIONS),
    "time_id": fields.String(required=False, description="Id of the time at which the fact occurs"),
    "time_type": fields.String(required=True, description="the type of the time", default="Time"),
    "location_id": fields.String(required=False, description="Id of the location or country in which the fact occurs"),
    "location_type": fields.String(required=True, description="the type of the time", enum=LOCATION_TYPES, default=LOCATION_TYPES[0]),
    "subject_id": fields.String(required=True, description="Id of the subject appears in the fact"),
    "object_id": fields.String(required=True, description="Id of the object appears in the fact"),
    "subject_type": fields.String(required=True, description="the type of the subject", enum=SUBJECT_TYPES),
    "object_type": fields.String(required=True, description= "The type of the object", enum=OBJECT_TYPES)
}
input_key_model = {
    "text": fields.String(required=True, description="Keyword for searching")
}