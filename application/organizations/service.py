from application import dao
from typing import List, Dict
from application.utilities.graph import serialize_node_to_dict

class OrganizationService:
    @staticmethod
    def get_all() -> List:
        query = """
        MATCH (org:Organization)
        RETURN org.entityID as entityID, org.name as name, org.des as description
        LIMIT 1000
        """
        return dao.run_read_query(query).data()

    @staticmethod
    def get_by_id(org_id):
        query = """
        MATCH (org:Organization{entityID: $org_id}) 
        RETURN org.entityID as entityID, org.name as name, org.des as description
        """
        return dao.run_read_query(query, org_id=org_id).data()

    @staticmethod
    def create(organization_properties):
        query = """
        CREATE (org:Organization $props)
        RETURN org.entityID as entityID, org.name as name, org.des as description
        """
        return dao.run_write_query(query, props= organization_properties).data()

    @staticmethod
    def update(organization_properties: Dict, org_id: str):
        query = """
            MATCH (org:Organization{entityID: $id_org})
            SET org = $props
            RETURN org.entityID as entityID, org.name as name, org.des as description
            """
        return dao.run_write_query(query, {"props":organization_properties, "id_org": org_id}).data()

    @staticmethod
    def is_in_news(org_id) -> bool:
        query = """
        MATCH (fact:Fact)-[]->(:Organization{entityID: $id_entity})
        RETURN count(fact) as numAppearance
        """
        result = dao.run_read_query(query, id_entity=org_id).data()
        if result[0]["numAppearance"] == 0:
            return False
        else:
            return True

    @staticmethod
    def delete(org_id):
        query = """
        MATCH (org: Organization{entityID: $id_entity})
        DELETE org
        """
        return dao.run_write_query(query, id_entity=org_id).data()

    @staticmethod
    def search(text_search: str):
        query = """
            MATCH(entity:Organization)
            WHERE entity.des CONTAINS $property
            RETURN entity.entityID as entityID, entity.name as name, entity.des as description
            """
        return dao.run_read_query(query, {"property": text_search}).data()

    @staticmethod
    def merge_nodes(set_entity_id: List[str]) -> Dict:
        query = """
                UNWIND $entity_id_set as entity_id 
                MATCH (node:Organization{entityID: entity_id})
                WITH collect(node) as nodes
                CALL apoc.refactor.mergeNodes(nodes, 
                        {properties: {entityID: "discard", name:"combine", des:"combine"},
                        mergeRels:True})
                YIELD node 
                RETURN node.entityID as entityID, node.name as name, node.des as description
                """
        result = dao.run_write_query(query, {"entity_id_set": list(set(set_entity_id))}).data()
        return result


