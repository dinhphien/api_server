from flask import request
from flask_restx import Namespace, Resource, abort, reqparse
from typing import List

from application.events.service import EventService
from application.events.model import event_model, entity_with_type_model
from application.utilities.wrap_functions import user_token_required, admin_token_required
from application.utilities.paginating import paginate_results

api = Namespace("Events", description="events related operations")
event = api.model("Event", event_model)
entity_type_news = api.model("Entity_Type_News", entity_with_type_model)

events_pagin_parser = reqparse.RequestParser()
events_pagin_parser.add_argument('start', location='args', type=int, help='The position to start getting results')
events_pagin_parser.add_argument('limit', location='args', type=int, help='Limit the number of news returned')
@api.route("/")
class EventsCollection(Resource):
    @api.doc(responses={200: 'OK'}, parser=events_pagin_parser)
    @user_token_required
    def get(self) -> List:
        """Get all Events
        Limit 1000 event entities
        """
        return paginate_results(events_pagin_parser, request.base_url, EventService.get_all)

    @api.doc(responses={200: 'OK', 201: 'Created', 400: 'Bad Request'})
    @api.expect(event, validate=True)
    @admin_token_required
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
            return {"message": "Unable to create because the event with this id already exists"}, 400


@api.route("/<string:id>")
class EventEntity(Resource):
    @api.doc(responses={200: 'OK', 404: 'Not Found'})
    @user_token_required
    def get(self, id):
        """Get a specific Event"""
        result = EventService.get_by_id(id)
        if not result:
            return {"message": "The event does not exist"}, 404
        else:
            return result[0]

    @api.doc(responses={200: 'OK', 404: 'Not Found', 400: 'Bad Request'})
    @api.expect(event)
    @admin_token_required
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

    @api.doc(responses={200: 'OK', 400: 'Bad Request'})
    @admin_token_required
    def delete(self, id):
        """Delete an event"""
        is_referenced = EventService.is_in_news(id)
        if is_referenced:
            return {"message": "Unable to delete because the event with this id is being referenced"}, 400
        else:
            EventService.delete(id)
            return {"message": "Successful"}, 200

@api.route("/search")
class SearchEventResource(Resource):
    @api.doc(responses={200: 'OK'}, parser=events_pagin_parser)
    @user_token_required
    def post(self):
        if "text" in request.json:
            text_search = request.json["text"]
        else:
            text_search = ' '
        return paginate_results(events_pagin_parser, request.base_url, EventService.search, text_search)

@api.route("/merge_nodes")
class MergeNodesResource(Resource):
    @api.expect(entity_type_news, validate=True)
    @admin_token_required
    def post(self):
        """Merge entities having the Event type
        *Keep entityID property of one entity, combine for the rest properties and also merge relations
        """
        set_entity_id = request.json["set_entity_id"]
        return EventService.merge_nodes(set_entity_id)









