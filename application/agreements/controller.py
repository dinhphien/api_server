from flask import request
from flask_restx import Namespace, Resource, abort
from typing import List

from application.agreements.service import AgreementService
from application.agreements.model import agreement_model, entity_with_type_model
from application.utilities.wrap_functions import user_token_required, admin_token_required

api = Namespace("Agreements", description="agreements related operations")
agreement = api.model("Agreement", agreement_model)
entity_type_news = api.model("Entity_Type_News", entity_with_type_model)


@api.route("/")
class AgreementsCollection(Resource):
    @user_token_required
    def get(self) -> List:
        """Get all Agreements
        Limit 1000 agreement entities
        """
        return AgreementService.get_all()

    @api.doc(responses={200: 'OK', 201: 'Created', 405: 'Method Not Allowed'})
    @api.expect(agreement, validate=True)
    @admin_token_required
    def post(self):
        """Create a new agreement
        Use this method to create a new agreement.
        * Send a JSON object with the detail in the request body.
        ```
        {
          "name": "Agreement Name",
          "entityID": "Agreement ID",
          "des": "Agreement Description"
        }
        ```
        """
        new_agreement = request.json
        agr = AgreementService.get_by_id(new_agreement['entityID'])
        if not agr:
            result = AgreementService.create(new_agreement)
            return result[0], 201
        else:
            return {"message": "Unable to create because the agreement with this id already exists"}, 405



@api.route("/<string:id>")
class AgreementEntity(Resource):
    @api.doc(responses={200: 'OK', 404: 'Not Found'})
    @user_token_required
    def get(self, id):
        """Get a specific Agreement"""
        result = AgreementService.get_by_id(id)
        if not result:
            return {"message": "The agreement does not exist"}, 404
        else:
            return result[0]

    @api.doc(responses={200: 'OK', 404:'Not Found', 400:'Bad Request'})
    @api.expect(agreement)
    @admin_token_required
    def put(self, id):
        """ Update an agreement
        Use this method to change properties of an agreement.
        * Send a JSON object with new properties in the request body.
        ```
        {
          "name": "New Agreement Name",
          "des": "New Agreement Description",
          "entityID": "Agreement ID"
        }
        ```
        * Specify the ID of the category to modify in the request URL path.
        """
        data = request.json
        if data["entityID"] != id:
            return {"message": "entityID property in the incoming json object and id parameter in the URL path are"
                               "not matched"}, 400
        agr = AgreementService.get_by_id(id)
        if not agr:
            return {"message": "The agreement does not exist"}, 404
        else:
            return AgreementService.update(data, id)

    @api.doc(responses={200: 'OK', 405: 'Method Not Allowed'})
    @admin_token_required
    def delete(self, id):
        """Delete an agreement"""
        is_referenced = AgreementService.is_in_news(id)
        if is_referenced:
            return {"message": "Unable to delete because the agreement with this id is being referenced"}, 405
        else:
            AgreementService.delete(id)
            return {"message": "Successful"}, 200

@api.route("/search")
class SearchAgreementResource(Resource):
    @api.doc(responses={200: 'OK', 404: 'Not Found'})
    @user_token_required
    def post(self):
        text_search = request.json["text"]
        return AgreementService.search(text_search)

@api.route("/merge_nodes")
class MergeNodesResource(Resource):
    @api.expect(entity_type_news, validate=True)
    @admin_token_required
    def post(self):
        """Merge entities having the same type
        *Keep entityID property of one entity, combine for the rest properties and also merge relations
        """
        set_entity_id = request.json["set_entity_id"]
        return AgreementService.merge_nodes(set_entity_id)







    
