from application import dao
from typing import List, Dict
from application.utilities.graph import serialize_node_to_dict

class CountryService:
    @staticmethod
    def get_all(start=0, limit=100) -> List:
        query = """
        MATCH (cty:Country)
        RETURN cty.entityID as entityID, cty.name as name, cty.des as description
        ORDER BY cty.entityID
        SKIP $start
        LIMIT $limit
        """
        return dao.run_read_query(query, start=start, limit=limit).data()

    @staticmethod
    def get_by_id(cty_id):
        query = """
        MATCH (cty:Country{entityID: $cty_id})
        RETURN cty.entityID as entityID, cty.name as name, cty.des as description
        """
        return dao.run_read_query(query, cty_id=cty_id).data()

    @staticmethod
    def create(country_properties):
        query = """
        CREATE (cty:Country $props)
        RETURN cty.entityID as entityID, cty.name as name, cty.des as description
        """
        return dao.run_write_query(query, props= country_properties).data()

    @staticmethod
    def update(country_properties: Dict, cty_id: str):
        query = """
            MATCH (cty:Country{entityID: $id_cty})
            SET cty = $props
            RETURN cty.entityID as entityID, cty.name as name, cty.des as description
            """
        return dao.run_write_query(query, {"props":country_properties, "id_cty": cty_id}).data()

    @staticmethod
    def is_in_news(cty_id) -> bool:
        query = """
        MATCH (fact:Fact)-[]->(:Country{entityID: $id_entity})
        RETURN count(fact) as numAppearance
        """
        result = dao.run_read_query(query, id_entity=cty_id).data()
        if result[0]["numAppearance"] == 0:
            return False
        else:
            return True

    @staticmethod
    def delete(cty_id):
        query = """
        MATCH (cty: Country{entityID: $id_entity})
        DELETE cty
        """
        return dao.run_write_query(query, id_entity=cty_id).data()

    @staticmethod
    def search(start=0, limit=100, *args, **kwargs):
        text_search = args[0]
        query = "CALL db.index.fulltext.queryNodes(" + "'countriesFullTextSearch', '" + text_search + \
                "') YIELD node, score  RETURN node.entityID as entityID, node.name as name," \
                "node.des as description, score ORDER BY score DESC"
        return dao.run_read_query(query).data()[start:start+limit]

    @staticmethod
    def merge_nodes(set_entity_id: List[str]) -> Dict:
        query = """
                UNWIND $entity_id_set as entity_id 
                MATCH (node:Country{entityID: entity_id})
                WITH collect(node) as nodes
                CALL apoc.refactor.mergeNodes(nodes, 
                        {properties: {entityID: "discard", name:"combine", des:"combine"},
                        mergeRels:True})
                YIELD node 
                RETURN node.entityID as entityID, node.name as name, node.des as description
                """
        result = dao.run_write_query(query, {"entity_id_set": list(set(set_entity_id))}).data()
        return result


