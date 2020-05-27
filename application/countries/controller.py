from flask import request
from flask_restx import Namespace, Resource
from typing import List

from application.countries.service import CountryService
from application.countries.model import country_model, entity_with_type_model

api = Namespace("Countries", description="countries related operations")
country = api.model("Countries", country_model)
entity_type_news = api.model("Entity_Type_News", entity_with_type_model)

@api.route("/")
class CountriesCollection(Resource):
    def get(self) -> List:
        """Get all Countries
        Limit 1000 country entities
        """
        return CountryService.get_all()

    @api.doc(responses={200: 'OK', 201: 'Created', 405: 'Method Not Allowed'})
    @api.expect(country, validate=True)
    def post(self):
        """Create a new country
        Use this method to create a new country.
        * Send a JSON object with the detail in the request body.
        ```
        {
          "name": "Country Name",
          "entityID": "Country ID",
          "des": "Country Description"
        }
        ```
        """
        new_country = request.json
        cty = CountryService.get_by_id(new_country['entityID'])
        if not cty:
            result = CountryService.create(new_country)
            return result[0], 201
        else:
            return {"message": "Unable to create because the country with this id already exists"}, 405


@api.route("/<string:id>")
class CountryEntity(Resource):
    @api.doc(responses={200: 'OK', 404: 'Not Found'})
    def get(self, id):
        """Get a specific Country"""
        result = CountryService.get_by_id(id)
        if not result:
            return {"message": "The country does not exist"}, 404
        else:
            return result[0]

    @api.doc(responses={200: 'OK', 404: 'Not Found', 400: 'Bad Request'})
    @api.expect(country)
    def put(self, id):
        """ Update a country
        Use this method to change properties of a country.
        * Send a JSON object with new properties in the request body.
        ```
        {
          "name": "New Country Name",
          "des": "New Country Description",
          "entityID": "Country ID"
        }
        ```
        * Specify the ID of the category to modify in the request URL path.
        """
        data = request.json
        if data["entityID"] != id:
            return {"message": "entityID property in the incoming json object and id parameter in the URL path are"
                               "not matched"}, 400
        agr = CountryService.get_by_id(id)
        if not agr:
            return {"message": "The country does not exist"}, 404
        else:
            return CountryService.update(data, id)

    @api.doc(responses={200: 'OK', 405: 'Method Not Allowed'})
    def delete(self, id):
        """Delete a country"""
        is_referenced = CountryService.is_in_news(id)
        if is_referenced:
            return {"message": "Unable to delete because the country with this id is being referenced"}, 405
        else:
            CountryService.delete(id)
            return {"message": "Successful"}, 200

    @api.route("/search")
    class SearchCountryResource(Resource):
        @api.doc(responses={200: 'OK', 404: 'Not Found'})
        def post(self):
            text_search = request.json["text"]
            return CountryService.search(text_search)

    @api.route("/merge_nodes")
    class MergeNodesResource(Resource):
        @api.expect(entity_type_news, validate=True)
        def post(self):
            """Merge entities having the same type
            *Keep entityID property of one entity, combine for the rest properties and also merge relations
            """
            set_entity_id = request.json["set_entity_id"]
            return CountryService.merge_nodes(set_entity_id)









