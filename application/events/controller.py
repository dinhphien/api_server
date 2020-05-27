from flask import request
from flask_restx import Namespace, Resource, abort
from typing import List

from application.events.service import EventService
from application.events.model import event_model, entity_with_type_model

api = Namespace("Events", description="events related operations")
event = api.model("Event", event_model)
entity_type_news = api.model("Entity_Type_News", entity_with_type_model)


@api.route("/")
class EventsCollection(Resource):
    def get(self) -> List:
        """Get all Events
        Limit 1000 event entities
        """
        return EventService.get_all()

    @api.doc(responses={200: 'OK', 201: 'Created', 405: 'Method Not Allowed'})
    @api.expect(event, validate=True)
    def post(self):
        """Create a new event
        Use this method to create a new event.
        * Send a JSON object with the detail in the request body.
        ```
        {
          "name": "Event Name",
          "entityID": "Event ID",
          "des": "Event Description"
        }
        ```
        """
        new_event = request.json
        evn = EventService.get_by_id(new_event['entityID'])
        if not evn:
            result = EventService.create(new_event)
            return result[0], 201
        else:
            return {"message": "Unable to create because the event with this id already exists"}, 405


@api.route("/<string:id>")
class EventEntity(Resource):
    @api.doc(responses={200: 'OK', 404: 'Not Found'})
    def get(self, id):
        """Get a specific Event"""
        result = EventService.get_by_id(id)
        if not result:
            return {"message": "The event does not exist"}, 404
        else:
            return result[0]

    @api.doc(responses={200: 'OK', 404: 'Not Found', 400: 'Bad Request'})
    @api.expect(event)
    def put(self, id):
        """ Update an event
        Use this method to change properties of an event.
        * Send a JSON object with new properties in the request body.
        ```
        {
          "name": "New Event Name",
          "des": "New Event Description",
          "entityID": "Event ID"
        }
        ```
        * Specify the ID of the category to modify in the request URL path.
        """
        data = request.json
        if data["entityID"] != id:
            return {"message": "entityID property in the incoming json object and id parameter in the URL path are"
                               "not matched"}, 400
        evn = EventService.get_by_id(id)
        if not evn:
            return {"message": "The event does not exist"}, 404
        else:
            return EventService.update(data, id)

    @api.doc(responses={200: 'OK', 405: 'Method Not Allowed'})
    def delete(self, id):
        """Delete an event"""
        is_referenced = EventService.is_in_news(id)
        if is_referenced:
            return {"message": "Unable to delete because the event with this id is being referenced"}, 405
        else:
            EventService.delete(id)
            return {"message": "Successful"}, 200

    @api.route("/search")
    class SearchEventResource(Resource):
        @api.doc(responses={200: 'OK', 404: 'Not Found'})
        def post(self):
            text_search = request.json["text"]
            return EventService.search(text_search)

    @api.route("/merge_nodes")
    class MergeNodesResource(Resource):
        @api.expect(entity_type_news, validate=True)
        def post(self):
            """Merge entities having the same type
            *Keep entityID property of one entity, combine for the rest properties and also merge relations
            """
            set_entity_id = request.json["set_entity_id"]
            return EventService.merge_nodes(set_entity_id)









