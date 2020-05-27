from application import dao
from typing import List, Dict
from application.utilities.graph import serialize_node_to_dict


class AgreementService:
    @staticmethod
    def get_all() -> List:
        query = """
        MATCH (agr:Agreement)
        RETURN agr.entityID as entityID, agr.name as name, agr.des as description
        LIMIT 1000
        """
        return dao.run_read_query(query).data()

    @staticmethod
    def get_by_id(agr_id):
        query = """
        MATCH (agr:Agreement{entityID: $agr_id}) 
        RETURN agr.entityID as entityID, agr.name as name, agr.des as description
        """
        return dao.run_read_query(query, agr_id=agr_id).data()

    @staticmethod
    def create(agreement_properties):
        query = """
        CREATE (agr:Agreement $props)
        RETURN agr.entityID as entityID, agr.name as name, agr.des as description
        """
        return dao.run_write_query(query, props= agreement_properties).data()

    @staticmethod
    def update(agreement_properties: Dict, agr_id: str):
        query = """
            MATCH (agr:Agreement{entityID: $id_agr})
            SET agr = $props
            RETURN agr.entityID as entityID, agr.name as name, agr.des as description
            """
        return dao.run_write_query(query, {"props":agreement_properties, "id_agr": agr_id}).data()

    @staticmethod
    def is_in_news(agr_id) -> bool:
        query = """
        MATCH (fact:Fact)-[]->(:Agreement{entityID: $id_entity})
        RETURN count(fact) as numAppearance
        """
        result = dao.run_read_query(query, id_entity=agr_id).data()
        if result[0]["numAppearance"] == 0:
            return False
        else:
            return True

    @staticmethod
    def delete(agr_id):
        query = """
        MATCH (agr: Agreement{entityID: $id_entity})
        DELETE agr
        """
        return dao.run_write_query(query, id_entity=agr_id).data()

    @staticmethod
    def search(text_search: str):
        query = """
        MATCH(entity:Agreement)
        WHERE entity.des CONTAINS $property
        RETURN entity.entityID as entityID, entity.name as name, entity.des as description
        """
        return dao.run_read_query(query, {"property": text_search}).data()

    @staticmethod
    def merge_nodes(set_entity_id: List[str]) -> Dict:
        query = """
            UNWIND $entity_id_set as entity_id 
            MATCH (node:Agreement{entityID: entity_id})
            WITH collect(node) as nodes
            CALL apoc.refactor.mergeNodes(nodes, 
                    {properties: {entityID: "discard", name:"combine", des:"combine"},
                    mergeRels:True})
            YIELD node 
            RETURN node.entityID as entityID, node.name as name, node.des as description
            """
        result = dao.run_write_query(query, {"entity_id_set": list(set(set_entity_id))}).data()
        return result


