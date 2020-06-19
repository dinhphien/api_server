from flask import request
from flask_restx import Namespace, Resource, abort, reqparse
from typing import List

from application.organizations.service import OrganizationService
from application.organizations.model import organization_model, entity_with_type_model
from application.utilities.wrap_functions import user_token_required, admin_token_required
from application.utilities.paginating import paginate_results

api = Namespace("Organizations", description="organizations related operations")
organization = api.model("Organization", organization_model)
entity_type_news = api.model("Entity_Type_News", entity_with_type_model)


orgs_pagin_parser = reqparse.RequestParser()
orgs_pagin_parser.add_argument('start', location='args', type=int, help='The position to start getting results')
orgs_pagin_parser.add_argument('limit', location='args', type=int, help='Limit the number of news returned')
@api.route("/")
class OrganizationsCollection(Resource):
    @api.doc(responses={200: 'OK'}, parser=orgs_pagin_parser)
    @user_token_required
    def get(self) -> List:
        """Get all Organizations
        Limit 1000 organization entities
        """
        # return OrganizationService.get_all()
        return paginate_results(orgs_pagin_parser, request.base_url, OrganizationService.get_all)

    @api.doc(responses={200: 'OK', 201: 'Created', 400: 'Bad Request'})
    @api.expect(organization, validate=True)
    @admin_token_required
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
            return {"message": "Unable to create because the organization with this id already exists"}, 400


@api.route("/<string:id>")
class OrganizationEntity(Resource):
    @api.doc(responses={200: 'OK', 404: 'Not Found'})
    @user_token_required
    def get(self, id):
        """Get a specific Organization"""
        result = OrganizationService.get_by_id(id)
        if not result:
            return {"message": "The organization does not exist"}, 404
        else:
            return result[0]

    @api.doc(responses={200: 'OK', 404: 'Not Found', 400: 'Bad Request'})
    @api.expect(organization)
    @admin_token_required
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

    @api.doc(responses={200: 'OK', 400: 'Bad Request'})
    @admin_token_required
    def delete(self, id):
        """Delete an organization"""
        is_referenced = OrganizationService.is_in_news(id)
        if is_referenced:
            return {"message": "Unable to delete because the organization with this id is being referenced"}, 400
        else:
            OrganizationService.delete(id)
            return {"message": "Successful"}, 200

@api.route("/search")
class SearchOrganizationResource(Resource):
    @api.doc(responses={200: 'OK'}, parser=orgs_pagin_parser)
    @user_token_required
    def post(self):
        if "text" in request.json:
            text_search = request.json["text"]
        else:
            text_search = ' '
        return paginate_results(orgs_pagin_parser, request.base_url, OrganizationService.search, text_search)

@api.route("/merge_nodes")
class MergeNodesResource(Resource):
    @api.expect(entity_type_news, validate=True)
    @admin_token_required
    def post(self):
        """Merge entities having the Organization type
        *Keep entityID property of one entity, combine for the rest properties and also merge relations
        """
        set_entity_id = request.json["set_entity_id"]
        return OrganizationService.merge_nodes(set_entity_id)









