from flask import request
from flask_restx import Namespace, Resource, abort
from typing import List
from datetime import datetime

from application.times.service import TimeService
from application.times.model import time_model, entity_with_type_model
from application.utilities.wrap_functions import user_token_required, admin_token_required


api = Namespace("Times", description="times related operations")
time = api.model("Time", time_model)
entity_type_news = api.model("Entity_Type_News", entity_with_type_model)

@api.route("/")
class TimesCollection(Resource):
    @user_token_required
    def get(self) -> List:
        """Get all Times
        Limit 1000 time entities
        """
        return TimeService.get_all()

    @api.doc(responses={200: 'OK', 201: 'Created', 405: 'Method Not Allowed', 400: 'Bad Request'})
    @api.expect(time, validate=True)
    @admin_token_required
    def post(self):
        """Create a new time
        Use this method to create a new time.
        * Send a JSON object with the detail in the request body.
        ```
        {
          "name": "Time Name",
          "entityID": "Time ID",
          "des": "Time Description"
        }
        ```
        """
        new_time = request.json
        tim = TimeService.get_by_id(new_time['entityID'])
        if not tim:
            try:
             formatedTime = datetime.strptime(new_time["des"], '%Y-%m-%d').date()
            except:
                return {"message": "Unable to create because the time description is not valid!"}, 400

            new_time["des"] = formatedTime
            result = TimeService.create(new_time)
            return result[0], 201
        else:
            return {"message": "Unable to create because the time with this id already exists"}, 405


@api.route("/<string:id>")
class TimeEntity(Resource):
    @api.doc(responses={200: 'OK', 404: 'Not Found'})
    @user_token_required
    def get(self, id):
        """Get a specific Time"""
        result = TimeService.get_by_id(id)
        if not result:
            return {"message": "The time does not exist"}, 404
        else:
            return result[0]

    @api.doc(responses={200: 'OK', 404: 'Not Found', 400: 'Bad Request'})
    @api.expect(time)
    @admin_token_required
    def put(self, id):
        """ Update a time
        Use this method to change properties of an time.
        * Send a JSON object with new properties in the request body.
        ```
        {
          "name": "New Time Name",
          "des": "New Time Description",
          "entityID": "Time ID"
        }
        ```
        * Specify the ID of the category to modify in the request URL path.
        """
        data = request.json
        if data["entityID"] != id:
            return {"message": "entityID property in the incoming json object and id parameter in the URL path are"
                               "not matched"}, 400
        tim = TimeService.get_by_id(id)
        if not tim:
            return {"message": "The time does not exist"}, 404
        else:
            try:
                formatedTime = datetime.strptime(data["des"], '%Y-%m-%d').date()
            except:
                return {"message": "Unable to create because the time description is not valid!"}, 400

            data["des"] = formatedTime
            return TimeService.update(data, id)

    @api.doc(responses={200: 'OK', 405: 'Method Not Allowed'})
    @admin_token_required
    def delete(self, id):
        """Delete a time"""
        is_referenced = TimeService.is_in_news(id)
        if is_referenced:
            return {"message": "Unable to delete because the time with this id is being referenced"}, 405
        else:
            TimeService.delete(id)
            return {"message": "Successful"}, 200

@api.route("/search")
class SearchTimeResource(Resource):
    @api.doc(responses={200: 'OK', 404: 'Not Found'})
    @user_token_required
    def post(self):
        text_search = request.json["text"]
        return TimeService.search(text_search)

@api.route("/merge_nodes")
class MergeNodesResource(Resource):
    @api.expect(entity_type_news, validate=True)
    @admin_token_required
    def post(self):
        """Merge entities having the same type
        *Keep entityID property of one entity, combine for the rest properties and also merge relations
        """
        set_entity_id = request.json["set_entity_id"]
        return TimeService.merge_nodes(set_entity_id)









