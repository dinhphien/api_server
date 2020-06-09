from typing import List, Dict
from application import dao
from application.utilities.graph import serialize_subgraph_to_dict, serialize_node_to_dict


class NewsService:
    @staticmethod
    def get_all() -> List:
        query = """
        MATCH (news:News) 
        RETURN news.entityID as entityID, news.link as link, news.topics as topics
        LIMIT 1000
        """
        return dao.run_read_query(query).data()

    @staticmethod
    def get_by_id(news_id: str):
        query = '''
        MATCH (news:News {entityID : $id})
        RETURN news.entityID as entityID, news.link as link, news.topics as topics
        '''
        return dao.run_read_query(query, id=news_id).data()

    @staticmethod
    def create(news_properties):
        query = """
        CREATE (news:News $props)
        RETURN news.entityID as entityID, news.link as link, news.topics as topics
        """
        return dao.run_write_query(query, props=news_properties).data()

    @staticmethod
    def update(news_properties: dict,news_id: str):
        query = """
        MATCH (news:News{entityID: $id_news})
        SET news = $props
        RETURN news.entityID as entityID, news.link as link, news.topics as topics
        """
        return dao.run_write_query(query, {"props": news_properties, "id_news": news_id}).data()

    @staticmethod
    def delete_by_id(news_id: str):
        query = """
        MATCH (news:News{entityID: $id_news})
        OPTIONAL MATCH (news)-[:HAS_FACT]->(fact:Fact)
        DETACH DELETE news, fact
        """
        return dao.run_write_query(query, id_news= news_id).data()

    @staticmethod
    def get_fact_by_id(fact_id: str):
        query = """
        MATCH (fact:Fact{entityID: $id_fact})
        RETURN fact
        """
        return dao.run_read_query(query, id_fact=fact_id).data()

    @staticmethod
    def create_fact(news_id: str, fact_data: Dict):
        query = "MATCH (news:News{entityID: $id_news}), " + \
                    "(sub:" + fact_data['subject_type']+ "{entityID: $id_subject}), " \
                    "(obj:" + fact_data['object_type'] + "{entityID: $id_object}) " \
                "OPTIONAL MATCH (loc:" + fact_data['location_type'] + "{entityID: $id_location})" \
                "OPTIONAL MATCH (time:" + fact_data['time_type'] + "{entityID: $id_time})" \
                "CREATE (fact:Fact{entityID: $id_fact}), " \
                    "(news)-[:HAS_FACT]->(fact), " \
                    "(fact)-[:HAS_SUBJECT_" + fact_data['relation'].replace(" ", "_").upper()+ "]->(sub)," \
                    "(fact)-[:HAS_OBJECT_" + fact_data["relation"].replace(" ", "_").upper()+ "]->(obj) " \
                "FOREACH (_ IN CASE WHEN loc IS NOT NULL THEN [1] ELSE [] END |" \
                    "CREATE (fact)-[:OCCURRED_IN]->(loc) )" \
                "FOREACH (_ IN CASE WHEN time IS NOT NULL THEN [1] ELSE [] END |" \
                    "CREATE (fact)-[:OCCURRED_ON]->(time) )" \
                "RETURN fact.entityID as factID"

        result = dao.run_write_query(query, {"id_news": news_id, "id_location":fact_data['location_id'],
                                   "id_time": fact_data["time_id"], "id_subject": fact_data["subject_id"],
                                   "id_object": fact_data["object_id"], "id_fact": fact_data["entityID"]}).data()
        return result

    @staticmethod
    def delete_fact(news_id: str, fact_id: str):
        query = """
        MATCH (:News{entityID: $id_news})-[:HAS_FACT]-(fact:Fact{entityID: $id_fact})
        DETACH DELETE fact
        """
        return dao.run_write_query(query, {"id_news": news_id, "id_fact": fact_id}).data()



    @staticmethod
    def get_all_relations_in_news(news_id: str) -> Dict:
        query = """
        MATCH (news:News{entityID: $id})-[:HAS_FACT]->(facts:Fact)-[rel]->(entity)
        RETURN facts, rel, entity
        """
        result = dao.run_read_query(query, id=news_id).graph()
        return serialize_subgraph_to_dict(result)

    @staticmethod
    def get_all_relations_in_set_news(set_news_id: List[str]) -> Dict:
        id_set_news = list(set(set_news_id))
        query = """
        UNWIND $set_news_id as news_id
        MATCH (news:News{entityID:news_id})-[:HAS_FACT]->(facts:Fact)-[rel]->(entity)
        RETURN facts, rel, entity
        """
        result = dao.run_read_query(query, set_news_id=id_set_news).graph()
        return serialize_subgraph_to_dict(result)

    # @staticmethod
    # def get_entity_relations_in_news(news_id: str, entity_id: str) -> Dict:
    #     query = """
    #     MATCH (news:News{entityID: $id_news})-[:HAS_FACT]->(facts:Fact)-[]->({entityID:$id_entity})
    #     WITH facts
    #     MATCH (facts)-[rel]->(entity)
    #     RETURN facts, rel, entity
    #     """
    #     result = dao.run_read_query(query, {"id_news" : news_id,"id_entity": entity_id}).graph()
    #     return serialize_subgraph_to_dict(result)

    # @staticmethod
    # def get_entity_relations_in_set_news(set_news_id: List[str], entity_id: str) -> Dict:
    #     id_set_news = list(set(set_news_id))
    #     query = """
    #     UNWIND $set_id_news as news_id
    #     MATCH (news:News{entityID: news_id})-[:HAS_FACT]->(facts:Fact)-[]->({entityID:$id_entity})
    #     WITH facts
    #     MATCH (facts)-[rel]->(entity)
    #     RETURN facts, rel, entity
    #     """
    #
    #     result = dao.run_read_query(query, {"set_id_news": id_set_news, "id_entity": entity_id}).graph()
    #     return serialize_subgraph_to_dict(result)

    @staticmethod
    def get_number_appearance_in_news(news_id: str, entity_id: str) -> Dict:
        query = """
        MATCH (news:News{entityID: $id_news})-[:HAS_FACT]->(facts:Fact)-[]->({entityID:$id_entity})
        RETURN count(facts) as numberAppearance
        """
        result = dao.run_read_query(query, {"id_news": news_id, "id_entity": entity_id}).data()
        return {"numberAppearance" : result[0]["numberAppearance"]}

    @staticmethod
    def get_number_appearance_in_set_news(set_news_id: List[str], entity_id: str) -> Dict:
        query = """
        UNWIND $set_id_news as news_id
        MATCH (news:News{entityID: news_id})-[:HAS_FACT]->(facts:Fact)-[]->({entityID:$id_entity})
        RETURN count(facts) as numberAppearance
        """
        result = dao.run_read_query(query, {"set_id_news": set_news_id, "id_entity": entity_id}).data()
        return {"numberAppearance": result[0]["numberAppearance"]}

    @staticmethod
    def get_entity_type_relations_in_news(news_id: str, entity_type: List[str]) -> Dict:
        query = """
        MATCH (news:News{entityID: $id_news})-[:HAS_FACT]->(facts:Fact)-[rel]->(entity)
        WHERE any( label IN labels(entity) WHERE label IN $type_entity)
        RETURN facts, rel, entity
        """
        result= dao.run_read_query(query, {"id_news": news_id, "type_entity": list(set(entity_type))}).graph()
        return serialize_subgraph_to_dict(result)

    @staticmethod
    def get_entity_type_relations_in_set_news(set_news_id: List[str], entity_type: List[str]) -> Dict:
        query = """
        UNWIND $set_id_news as news_id
        MATCH (news:News{entityID: news_id})-[:HAS_FACT]->(facts:Fact)-[rel]->(entity)
        WHERE any( label IN labels(entity) WHERE label IN $type_entity)
        RETURN facts, rel, entity
        """
        result= dao.run_read_query(query, {"set_id_news": list(set(set_news_id)),
                                        "type_entity": list(set(entity_type))}).graph()
        return serialize_subgraph_to_dict(result)

    @staticmethod
    def get_entity_individual_relations_in_news(news_id: str, entity_id: str)->Dict:
        query = """
        MATCH (news:News{entityID: $id_news})-[:HAS_FACT]->(fact:Fact)-[]->({entityID:$id_entity})
        WITH fact
        MATCH (fact)-[rel]->(entity)
        RETURN fact, rel, entity
        """
        result = dao.run_read_query(query, {"id_news": news_id, "id_entity": entity_id}).graph()
        return serialize_subgraph_to_dict(result)

    @staticmethod
    def get_entity_individual_relations_in_set_news(set_news_id: List[str], entity_id:str)->Dict:
        query = """
        UNWIND $set_id_news as news_id
        MATCH (news:News{entityID: news_id})-[:HAS_FACT]->(facts:Fact)-[]->({entityID:$id_entity})
        WITH facts
        MATCH (facts)-[rel]->(entity)
        RETURN facts, rel, entity
        """
        result = dao.run_read_query(query, {"set_id_news": list(set(set_news_id)),
                                            "id_entity": entity_id}).graph()
        return serialize_subgraph_to_dict(result)




    @staticmethod
    def merge_nodes(set_entity_id: List[str], entity_type: str) -> Dict:
        query = """
        UNWIND $entity_id_set as entity_id 
        MATCH (node {entityID: entity_id})
        WHERE $label IN labels(node)
        WITH collect(node) as nodes
        CALL apoc.refactor.mergeNodes(nodes, 
                {properties: {entityID: "discard", name:"combine", des:"combine"},
                mergeRels:True})
        YIELD node 
        RETURN node
        """
        result = dao.run_write_query(query, {"entity_id_set" :list(set(set_entity_id)), "label": entity_type}).single()
        if (result):
            merged_node = result["node"]
            return serialize_node_to_dict(merged_node)
        else:
            return {}

    @staticmethod
    def search_news(input_text: str)-> List:
        query = """
        MATCH(news:News)
        WHERE news.link CONTAINS $property
        RETURN news.entityID as entityID, news.link as link, news.topics as topics
        """
        return dao.run_read_query(query, {"property": input_text}).data()

    @staticmethod
    def search_entity(input_type_entity, input_text)-> List:
        query = """
        MATCH(entity)
        WHERE any( label IN labels(entity) WHERE label IN $type_entity) AND entity.des CONTAINS $property
        RETURN entity.entityID as entityID, entity.name as name, entity.des as description
        """
        return dao.run_read_query(query, {"type_entity": input_type_entity, "property": input_text}).data()

    @staticmethod
    def get_detailed_facts_in_news(news_id: str):
        query= """
        MATCH(news:News{entityID: $id_news})-[:HAS_FACT]->(facts:Fact)
        WITH facts
        MATCH (facts)-[r]->(entity)
        RETURN facts.entityID as factID, collect(type(r)) as predicate, collect(entity.entityID) as entityID
        """
        result = dao.run_read_query(query, {"id_news": news_id}).data()
        facts = []
        for res in result:
            detailed_fact = {"timeID": None, "locationID": None }
            detailed_fact["factID"] = res["factID"]
            predicate = res["predicate"]
            for pre in predicate:
                if pre == "OCCURRED_ON":
                    detailed_fact["timeID"] = res["entityID"][predicate.index(pre)]
                elif pre == "OCCURRED_IN":
                    detailed_fact["locationID"] = res["entityID"][predicate.index(pre)]
                elif pre.find("HAS_SUBJECT") > -1:
                    detailed_fact["subjectID"] = res["entityID"][predicate.index(pre)]
                    relation = pre[len("HAS_SUBJECT") + 1:].replace("_", " ")
                    detailed_fact["relation"] = relation
                else:
                    detailed_fact["objectID"] = res["entityID"][predicate.index(pre)]
            facts.append(detailed_fact)
        return facts




