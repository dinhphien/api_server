from flask import request
from flask_restx import Namespace, Resource, abort
from typing import List

from application.organizations.service import OrganizationService
from application.organizations.model import organization_model, entity_with_type_model

api = Namespace("Organizations", description="organizations related operations")
organization = api.model("Organization", organization_model)
entity_type_news = api.model("Entity_Type_News", entity_with_type_model)

@api.route("/")
class OrganizationsCollection(Resource):
    def get(self) -> List:
        """Get all Organizations
        Limit 1000 organization entities
        """
        return OrganizationService.get_all()

    @api.doc(responses={200: 'OK', 201: 'Created', 405: 'Method Not Allowed'})
    @api.expect(organization, validate=True)
    def post(self):
        """Create a new organization
        Use this method to create a new organization.
        * Send a JSON object with the detail in the request body.
        ```
        {
          "name": "Organization Name",
          "entityID": "Organization ID",
          "des": "Organization Description"
        }
        ```
        """
        new_organization = request.json
        org = OrganizationService.get_by_id(new_organization['entityID'])
        if not org:
            result = OrganizationService.create(new_organization)
            return result[0], 201
        else:
            return {"message": "Unable to create because the organization with this id already exists"}, 405


@api.route("/<string:id>")
class OrganizationEntity(Resource):
    @api.doc(responses={200: 'OK', 404: 'Not Found'})
    def get(self, id):
        """Get a specific Organization"""
        result = OrganizationService.get_by_id(id)
        if not result:
            return {"message": "The organization does not exist"}, 404
        else:
            return result[0]

    @api.doc(responses={200: 'OK', 404: 'Not Found', 400: 'Bad Request'})
    @api.expect(organization)
    def put(self, id):
        """ Update an organization
        Use this method to change properties of an organization.
        * Send a JSON object with new properties in the request body.
        ```
        {
          "name": "New Organization Name",
          "des": "New Organization Description",
          "entityID": "Organization ID"
        }
        ```
        * Specify the ID of the category to modify in the request URL path.
        """
        data = request.json
        if data["entityID"] != id:
            return {"message": "entityID property in the incoming json object and id parameter in the URL path are"
                               "not matched"}, 400
        org = OrganizationService.get_by_id(id)
        if not org:
            return {"message": "The organization does not exist"}, 404
        else:
            return OrganizationService.update(data, id)

    @api.doc(responses={200: 'OK', 405: 'Method Not Allowed'})
    def delete(self, id):
        """Delete an organization"""
        is_referenced = OrganizationService.is_in_news(id)
        if is_referenced:
            return {"message": "Unable to delete because the organization with this id is being referenced"}, 405
        else:
            OrganizationService.delete(id)
            return {"message": "Successful"}, 200

    @api.route("/search")
    class SearchOrganizationResource(Resource):
        @api.doc(responses={200: 'OK', 404: 'Not Found'})
        def post(self):
            text_search = request.json["text"]
            return OrganizationService.search(text_search)

    @api.route("/merge_nodes")
    class MergeNodesResource(Resource):
        @api.expect(entity_type_news, validate=True)
        def post(self):
            """Merge entities having the same type
            *Keep entityID property of one entity, combine for the rest properties and also merge relations
            """
            set_entity_id = request.json["set_entity_id"]
            return OrganizationService.merge_nodes(set_entity_id)









