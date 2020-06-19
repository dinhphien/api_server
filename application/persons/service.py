from application import dao
from typing import List, Dict
from application.utilities.graph import serialize_node_to_dict

class PersonService:
    @staticmethod
    def get_all(start=0, limit=100) -> List:
        query = """
        MATCH (per:Person)
        RETURN per.entityID as entityID, per.name as name, per.des as description
        ORDER BY per.entityID
        SKIP $start
        LIMIT $limit
        """
        return dao.run_read_query(query, start=start, limit=limit).data()

    @staticmethod
    def get_by_id(per_id):
        query = """
        MATCH (per:Person{entityID: $per_id}) 
        RETURN per.entityID as entityID, per.name as name, per.des as description
        """
        return dao.run_read_query(query, per_id=per_id).data()

    @staticmethod
    def create(person_properties):
        query = """
        CREATE (per:Person $props)
        RETURN per.entityID as entityID, per.name as name, per.des as description
        """
        return dao.run_write_query(query, props= person_properties).data()

    @staticmethod
    def update(person_properties: Dict, per_id: str):
        query = """
            MATCH (per:Person{entityID: $id_per})
            SET per = $props
            RETURN per.entityID as entityID, per.name as name, per.des as description
            """
        return dao.run_write_query(query, {"props":person_properties, "id_per": per_id}).data()

    @staticmethod
    def is_in_news(per_id) -> bool:
        query = """
        MATCH (fact:Fact)-[]->(:Person{entityID: $id_entity})
        RETURN count(fact) as numAppearance
        """
        result = dao.run_read_query(query, id_entity=per_id).data()
        if result[0]["numAppearance"] == 0:
            return False
        else:
            return True

    @staticmethod
    def delete(per_id):
        query = """
        MATCH (per: Person{entityID: $id_entity})
        DELETE per
        """
        return dao.run_write_query(query, id_entity=per_id).data()

    @staticmethod
    def search(start=0, limit=100, *args, **kwargs):
        text_search = args[0]
        query = "CALL db.index.fulltext.queryNodes(" + "'personsFullTextSearch', '" + text_search + \
                "') YIELD node, score  RETURN node.entityID as entityID, node.name as name," \
                "node.des as description, score ORDER BY score DESC"
        return dao.run_read_query(query).data()[start:start+limit]

    @staticmethod
    def merge_nodes(set_entity_id: List[str]) -> Dict:
        query = """
                UNWIND $entity_id_set as entity_id 
                MATCH (node:Person{entityID: entity_id})
                WITH collect(node) as nodes
                CALL apoc.refactor.mergeNodes(nodes, 
                        {properties: {entityID: "discard", name:"combine", des:"combine"},
                        mergeRels:True})
                YIELD node 
                RETURN node.entityID as entityID, node.name as name, node.des as description
                """
        return dao.run_write_query(query, {"entity_id_set": list(set(set_entity_id))}).data()



