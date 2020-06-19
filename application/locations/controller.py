from flask import request
from flask_restx import Namespace, Resource, abort, reqparse
from typing import List

from application.locations.service import LocationService
from application.locations.model import location_model, entity_with_type_model
from application.utilities.wrap_functions import user_token_required, admin_token_required
from application.utilities.paginating import paginate_results

api = Namespace("Locations", description="locations related operations")
location = api.model("Location", location_model)
entity_type_news = api.model("Entity_Type_News", entity_with_type_model)

locations_pagin_parser = reqparse.RequestParser()
locations_pagin_parser.add_argument('start', location='args', type=int, help='The position to start getting results')
locations_pagin_parser.add_argument('limit', location='args', type=int, help='Limit the number of news returned')
@api.route("/")
class LocationsCollection(Resource):
    @api.doc(responses={200: 'OK'}, parser=locations_pagin_parser)
    @user_token_required
    def get(self) -> List:
        """Get all Locations
        Limit 1000 location entities
        """
        return paginate_results(locations_pagin_parser, request.base_url, LocationService.get_all)

    @api.doc(responses={200: 'OK', 201: 'Created', 400: 'Bad Request'})
    @api.expect(location, validate=True)
    @admin_token_required
    def post(self):
        """Create a new location
        Use this method to create a new location.
        * Send a JSON object with the detail in the request body.
        ```
        {
          "name": "Location Name",
          "entityID": "Location ID",
          "des": "Location Description"
        }
        ```
        """
        new_location = request.json
        loc = LocationService.get_by_id(new_location['entityID'])
        if not loc:
            result = LocationService.create(new_location)
            return result[0], 201
        else:
            return {"message": "Unable to create because the location with this id already exists"}, 400


@api.route("/<string:id>")
class LocationEntity(Resource):
    @api.doc(responses={200: 'OK', 404: 'Not Found'})
    @user_token_required
    def get(self, id):
        """Get a specific Location"""
        result = LocationService.get_by_id(id)
        if not result:
            return {"message": "The location does not exist"}, 404
        else:
            return result[0]

    @api.doc(responses={200: 'OK', 404: 'Not Found', 400: 'Bad Request'})
    @api.expect(location)
    @admin_token_required
    def put(self, id):
        """ Update an location
        Use this method to change properties of an location.
        * Send a JSON object with new properties in the request body.
        ```
        {
          "name": "New Location Name",
          "des": "New Location Description",
          "entityID": "Location ID"
        }
        ```
        * Specify the ID of the category to modify in the request URL path.
        """
        data = request.json
        if data["entityID"] != id:
            return {"message": "entityID property in the incoming json object and id parameter in the URL path are"
                               "not matched"}, 400
        loc = LocationService.get_by_id(id)
        if not loc:
            return {"message": "The location does not exist"}, 404
        else:
            return LocationService.update(data, id)

    @api.doc(responses={200: 'OK', 400: 'Bad Request'})
    @admin_token_required
    def delete(self, id):
        """Delete an location"""
        is_referenced = LocationService.is_in_news(id)
        if is_referenced:
            return {"message": "Unable to delete because the location with this id is being referenced"}, 400
        else:
            LocationService.delete(id)
            return {"message": "Successful"}, 200

@api.route("/search")
class SearchLocationResource(Resource):
    @api.doc(responses={200: 'OK'}, parser=locations_pagin_parser)
    @user_token_required
    def post(self):
        if "text" in request.json:
            text_search = request.json["text"]
        else:
            text_search = ' '
        return paginate_results(locations_pagin_parser, request.base_url, LocationService.search, text_search)

@api.route("/merge_nodes")
class MergeNodesResource(Resource):
    @api.expect(entity_type_news, validate=True)
    @admin_token_required
    def post(self):
        """Merge entities having the Location type
        *Keep entityID property of one entity, combine for the rest properties and also merge relations
        """
        set_entity_id = request.json["set_entity_id"]
        return LocationService.merge_nodes(set_entity_id)









