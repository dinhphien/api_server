from flask_restx import Namespace, Resource, reqparse
from flask import Response, request, jsonify, json


from .service import NewsService
from .model import news_model, set_news_model, types_entity_model, \
    types_entity_set_news_model, entity_with_type_model, fact_model, \
    input_key_model,ENTITY_TYPES
from application.utilities.wrap_functions import user_token_required, admin_token_required
from application.utilities.paginating import paginate_results
from application.config import START_PAGIN, LIMIT_PAGIN
from typing import List

api = Namespace("News", description="news related operations")
news = api.model("News", news_model)
news_set = api.model("Set_News", set_news_model)
types_entity = api.model("Types_News", types_entity_model)
types_entity_set_news = api.model("Types_Entity_Set_News", types_entity_set_news_model)
entity_type_news = api.model("Entity_Type_News", entity_with_type_model)
keyword_search = api.model("Keyword_Search", input_key_model)
fact = api.model("Fact", fact_model)

news_pagin_parser = reqparse.RequestParser()
news_pagin_parser.add_argument('start', location='args', type=int, help='The position to start getting results')
news_pagin_parser.add_argument('limit', location='args', type=int, help='Limit the number of news returned')
@api.route("/")
class NewsResourceList(Resource):
    @api.doc(responses={200: 'OK'}, parser=news_pagin_parser)
    @user_token_required
    def get(self) -> List:
        """Get all News
        Limit 1000 news entities.
        """
        return paginate_results(news_pagin_parser, request.base_url, NewsService.get_all)


    @api.doc(responses={200: 'OK', 201: 'Created', 400: 'Bad Request'})
    @api.expect(news, validate=True)
    @admin_token_required
    def post(self):
        """Create a news
        Use this method to create a news.
        * Send a JSON object with the detail in the request body.
        ```
        {
          "link": "News URL",
          "entityID": "News ID",
          "topics": "the subjects of news"
        }
        ```
        """
        news_data = request.json
        agr = NewsService.get_by_id(news_data['entityID'])
        if not agr:
            result = NewsService.create(news_data)
            return result[0], 201
        else:
            return {"message": "Unable to create because the news with this id already exists"}, 400



@api.route("/<string:id>")
class NewsResource(Resource):

    @api.doc(responses={200: 'OK', 404: 'Not Found'})
    @user_token_required
    def get(self, id):
        """Get a specific News"""
        result = NewsService.get_by_id(id)
        if not result:
            return {"message": "This news does not exist"}, 404
        else:
            return result[0]

    @api.doc(responses={200: 'OK', 404: 'Not Found', 400: 'Bad Request'})
    @api.expect(news, validate=True)
    @admin_token_required
    def put(self, id):
        """ Update a news
        Use this method to change properties of the news.
        * Send a JSON object with new properties in the request body.
        ```
        {
          "link": "News URL",
          "topics": "News subjects",
          "entityID": "News ID"
        }
        ```
        * Specify the ID of the category to modify in the request URL path.
        """
        data = request.json
        if data["entityID"] != id:
            return {"message": "entityID property in the incoming json object and id parameter in the URL path are"
                               " not matched"}, 400
        news = NewsService.get_by_id(id)
        if not news:
            return {"message": "The news does not exist"}, 404
        else:
            return NewsService.update(data, id)

    @api.doc(responses={200: 'OK'})
    def delete(self, id):
        """Delete a news"""
        NewsService.delete_by_id(id)
        return {"message": "Successful"}

@api.route("/<string:news_id>/facts")
class CollectionFactsNews(Resource):
    @api.doc(responses={200: 'OK'})
    @user_token_required
    def get(self, news_id):
        """ Get detailed facts in a news
        """
        return NewsService.get_detailed_facts_in_news(news_id)



    @api.doc(responses={200: 'OK', 404: 'Not Found', 400: 'Bad Request'})
    @api.expect(fact, validate=True)
    @admin_token_required
    def post(self, news_id):
        """ Add fact to an news
        Use this method to add a fact to an news.
        * Send a JSON object with the following properties in the request body.
        ```
        {
          "entityID": "Id of the fact",
          "relation": "relation between subject and object of the fact",
          "time_id": "Id of the time at which the fact appeared",
          "time_type": "Time",
          "location_id": "Id of the location in which the fact occurred",
          "location_type": "Location or Country",
          "subject_id": "Id of the Subject",
          "object_id": "Id of the Object",
          "subject_type": "The category of the Subject",
          "object_type": "The category of the Object"

        }
        ```
        """
        fact_data = request.json
        relation_type = (fact_data['subject_type'], fact_data['relation'], fact_data['object_type'])
        # check whether or not the relation type is supported
        # if
        #
        fact = NewsService.get_fact_by_id(fact_data["entityID"])
        if not fact:
            result = NewsService.create_fact(news_id, fact_data)
            if not result:
                return {"message": "One of these arguments news_id, subject_id, subject_id does not exist"}, 404
            else:
                return result[0]
        else:
            return {"message": "The fact identified by this entityID already exists"}, 400



@api.route("/<string:news_id>/facts/<string:fact_id>")
class FactNews(Resource):
    # def put(self, news_id, fact_id):
    #     """update a fact within a news"""
    #     pass
    @api.doc(responses={200: 'OK'})
    @admin_token_required
    def delete(self, news_id, fact_id):
        """delete a fact within a news"""
        NewsService.delete_fact(news_id, fact_id)
        return {"message": "Successful"}

# @api.route("/<string:news_id>/facts")
# class FactsInNews(Resource):
#     @user_token_required
#     def get(self, news_id):
#         return NewsService.get_detailed_facts_in_news(news_id)


@api.route("/<string:news_id>/relations")
class NewsRelations(Resource):
    @api.doc(responses={200: 'OK'})
    @user_token_required
    def get(self, news_id):
        """Get all entities and relations in a news"""

        return NewsService.get_all_relations_in_news(news_id)


# @api.route("/<string:news_id>/relations/<string:entity_id>")
# class EntityNewsRelations(Resource):
#     def get(self, news_id, entity_id):
#         """Get all relations of an entity within a news"""
#         return NewsService.get_entity_relations_in_news(news_id,entity_id)


@api.route("/relations")

class SetNewsRelations(Resource):
    @api.doc(responses={200: 'OK'})
    @api.expect(news_set, validate=True)
    @user_token_required
    def post(self):
        """ Get all entities and relations in a set of news
        Use this method to get all entities and relations in a set of news
        * Send a JSON object with the following properties in the request body.
        ```
        {
          "set_news_id": "set ids of news"
        }
        ```
        """
        set_news_id = request.json["set_news_id"]
        return NewsService.get_all_relations_in_set_news(set_news_id)


# @api.route("/relations/<string:entity_id>")
# class EntitySetNewsRelations(Resource):
#     @api.expect(news_set, validate=True)
#     def post(self, entity_id):
#         """Get all relations of an entity within a set of news"""
#         set_news_id = request.json["set_news_id"]
#         return NewsService.get_entity_relations_in_set_news(set_news_id,entity_id)


@api.route("/<string:news_id>/appearance/<string:entity_id>")
class EntityAppearanceNews(Resource):
    @api.doc(responses={200: 'OK'})
    @user_token_required
    def get(self, news_id, entity_id):
        """Get the number of times an entity occurs in a news"""
        return NewsService.get_number_appearance_in_news(news_id, entity_id)


@api.route("/appearance/<string:entity_id>")
class EntityAppearanceNewsSet(Resource):
    @api.doc(responses={200: 'OK', 400: 'Bad Request'})
    @api.expect(news_set, validate=True)
    @user_token_required
    def post(self, entity_id):
        """ Get the number of times an entity occurs in a set of news
       Use this method to get the number of times an entity occurs in a set of news
       * Send a JSON object with the following properties in the request body.
       ```
       {
         "set_news_id": "set ids of news"
       }
       ```
       """
        set_news_id = request.json["set_news_id"]
        return NewsService.get_number_appearance_in_set_news(set_news_id, entity_id)

@api.route("/<string:news_id>/type/relations")
class EntityRelationTypeNews(Resource):
    @api.doc(responses={200: 'OK', 400: 'Bad Request'})
    @api.expect(types_entity, validate=True)
    @user_token_required
    def post(self, news_id):

        """ Get all entities belongs to some specific types and their relations in a news
       Use this method to get all entities belongs to some specific types and their relations in a news
       * Send a JSON object with the following properties in the request body.
       ```
       {
         "set_entity_type": "set entity types"
       }
       ```
       """
        set_entity_types = request.json["set_entity_types"]
        return NewsService.get_entity_type_relations_in_news(news_id, set_entity_types)

@api.route("/<string:news_id>/entity/<string:entity_id>/relations")
class EntityIndividualRelationNews(Resource):
    @api.doc(responses={200: 'OK', 400: 'Bad Request'})
    @user_token_required
    def get(self, news_id, entity_id):
        """Get a specified entity and its relations in a news"""
        return NewsService.get_entity_individual_relations_in_news(news_id, entity_id)

@api.route("/type/relations")
class EntityRelationTypeSetNews(Resource):
    @api.doc(responses={200: 'OK', 400: 'Bad Request'})
    @api.expect(types_entity_set_news, validate=True)
    @user_token_required
    def post(self):
        """ Get all entities belongs to some specific types and their relations in a set of news
       Use this method to get all entities belongs to some specific types and their relations in a set of news
       * Send a JSON object with the following properties in the request body.
       ```
       {
        "set_news_id": "set Ids of news"
         "set_entity_type": "set entity types"
       }
       ```
       """
        set_news_id = request.json["set_news_id"]
        set_entity_types = request.json["set_entity_types"]
        return NewsService.get_entity_type_relations_in_set_news(set_news_id, set_entity_types)

@api.route("/entity/<string:entity_id>/relations")
class EntityIndividualSetNews(Resource):
    @api.doc(responses={200: 'OK', 400: 'Bad Request'})
    @api.expect(news_set, validate=True)
    @user_token_required
    def post(self, entity_id):
        """ Get a specified entity and its relations in a set of news
       Use this method to get a specified entity and its relations in a set of news
       * Send a JSON object with the following properties in the request body.
       ```
       {
         "set_news_id": "set Ids of news"
       }
       ```
       """

        set_news_id = request.json["set_news_id"]
        return NewsService.get_entity_individual_relations_in_set_news(set_news_id, entity_id)


@api.route("/merge_nodes")
class MergeNodesResource(Resource):
    @api.doc(responses={200: 'OK', 400: 'Bad Request'})
    @api.expect(entity_type_news, validate=True)
    @admin_token_required
    def post(self):
        """Merge entities having the same type
        *Keep entityID property of one entity, combine for the rest properties and also merge relations
        """
        set_entity_id = request.json["set_entity_id"]
        entity_type = request.json["entity_type"]
        return NewsService.merge_nodes(set_entity_id, entity_type)


@api.route("/search")
class SearchNewsResource(Resource):
    @api.doc(responses={200: 'OK'}, parser=news_pagin_parser)
    @user_token_required
    # @api.expect(keyword_search, validate=True)
    def post(self):
        if "text" in request.json:
            text_search = request.json["text"]
        else:
            text_search = ' '
        return paginate_results(news_pagin_parser, request.base_url, NewsService.search_news, text_search)



@api.route("/entity/search")
class SearchEntityResource(Resource):
    @api.doc(responses={200: 'OK', 404: 'Not Found'})
    @user_token_required
    def post(self):
        text_search = request.json["text"]
        type_entity = request.json["type_entity"]
        if type_entity not in ENTITY_TYPES:
            return {"message": "entity type not found!"}, 404
        return NewsService.search_entity(type_entity, text_search)









