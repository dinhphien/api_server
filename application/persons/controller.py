from flask import request
from flask_restx import Namespace, Resource, abort
from typing import List

from application.persons.service import PersonService
from application.persons.model import person_model, entity_with_type_model

api = Namespace("Persons", description="persons related operations")
person = api.model("Person", person_model)
entity_type_news = api.model("Entity_Type_News", entity_with_type_model)


@api.route("/")
class PersonsCollection(Resource):
    def get(self) -> List:
        """Get all Persons
        Limit 1000 person entities
        """
        return PersonService.get_all()

    @api.doc(responses={200: 'OK', 201: 'Created', 405: 'Method Not Allowed'})
    @api.expect(person, validate=True)
    def post(self):
        """Create a new person
        Use this method to create a new person.
        * Send a JSON object with the detail in the request body.
        ```
        {
          "name": "Person Name",
          "entityID": "Person ID",
          "des": "Person Description"
        }
        ```
        """
        new_person = request.json
        per = PersonService.get_by_id(new_person['entityID'])
        if not per:
            result = PersonService.create(new_person)
            return result[0], 201
        else:
            return {"message": "Unable to create because the person with this id already exists"}, 405


@api.route("/<string:id>")
class PersonEntity(Resource):
    @api.doc(responses={200: 'OK', 404: 'Not Found'})
    def get(self, id):
        """Get a specific Person"""
        result = PersonService.get_by_id(id)
        if not result:
            return {"message": "The person does not exist"}, 404
        else:
            return result[0]

    @api.doc(responses={200: 'OK', 404: 'Not Found', 400: 'Bad Request'})
    @api.expect(person)
    def put(self, id):
        """ Update a person
        Use this method to change properties of a person.
        * Send a JSON object with new properties in the request body.
        ```
        {
          "name": "New Person Name",
          "des": "New Person Description",
          "entityID": "Person ID"
        }
        ```
        * Specify the ID of the category to modify in the request URL path.
        """
        data = request.json
        if data["entityID"] != id:
            return {"message": "entityID property in the incoming json object and id parameter in the URL path are"
                               "not matched"}, 400
        per = PersonService.get_by_id(id)
        if not per:
            return {"message": "The person does not exist"}, 404
        else:
            return PersonService.update(data, id)

    @api.doc(responses={200: 'OK', 405: 'Method Not Allowed'})
    def delete(self, id):
        """Delete a person"""
        is_referenced = PersonService.is_in_news(id)
        if is_referenced:
            return {"message": "Unable to delete because the person with this id is being referenced"}, 405
        else:
            PersonService.delete(id)
            return {"message": "Successful"}, 200

    @api.route("/search")
    class SearchPersonResource(Resource):
        @api.doc(responses={200: 'OK', 404: 'Not Found'})
        def post(self):
            text_search = request.json["text"]
            return PersonService.search(text_search)

    @api.route("/merge_nodes")
    class MergeNodesResource(Resource):
        @api.expect(entity_type_news, validate=True)
        def post(self):
            """Merge entities having the same type
            *Keep entityID property of one entity, combine for the rest properties and also merge relations
            """
            set_entity_id = request.json["set_entity_id"]
            return PersonService.merge_nodes(set_entity_id)









