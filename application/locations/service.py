from application import dao
from typing import List, Dict
from application.utilities.graph import serialize_node_to_dict

class LocationService:
    @staticmethod
    def get_all(start=0, limit=100) -> List:
        query = """
        MATCH (loc:Location)
        RETURN loc.entityID as entityID, loc.name as name, loc.des as description
        ORDER BY loc.entityID
        SKIP $start
        LIMIT $limit
        """
        return dao.run_read_query(query, start=start, limit=limit).data()

    @staticmethod
    def get_by_id(loc_id):
        query = """
        MATCH (loc:Location{entityID: $loc_id}) 
        RETURN loc.entityID as entityID, loc.name as name, loc.des as description
        """
        return dao.run_read_query(query, loc_id=loc_id).data()

    @staticmethod
    def create(location_properties):
        query = """
        CREATE (loc:Location $props)
        RETURN loc.entityID as entityID, loc.name as name, loc.des as description
        """
        return dao.run_write_query(query, props= location_properties).data()

    @staticmethod
    def update(location_properties: Dict, loc_id: str):
        query = """
            MATCH (loc:Location{entityID: $id_loc})
            SET loc = $props
            RETURN loc.entityID as entityID, loc.name as name, loc.des as description
            """
        return dao.run_write_query(query, {"props":location_properties, "id_loc": loc_id}).data()

    @staticmethod
    def is_in_news(loc_id) -> bool:
        query = """
        MATCH (fact:Fact)-[]->(:Location{entityID: $id_entity})
        RETURN count(fact) as numAppearance
        """
        result = dao.run_read_query(query, id_entity=loc_id).data()
        if result[0]["numAppearance"] == 0:
            return False
        else:
            return True

    @staticmethod
    def delete(loc_id):
        query = """
        MATCH (loc: Location{entityID: $id_entity})
        DELETE loc
        """
        return dao.run_write_query(query, id_entity=loc_id).data()

    @staticmethod
    def search(start=0, limit=100, *args, **kwargs):
        text_search = args[0]
        query = "CALL db.index.fulltext.queryNodes(" + "'locationsFullTextSearch', '" + text_search + \
                "') YIELD node, score  RETURN node.entityID as entityID, node.name as name," \
                "node.des as description, score ORDER BY score DESC"
        return dao.run_read_query(query).data()[start:start+limit]

    @staticmethod
    def merge_nodes(set_entity_id: List[str]) -> Dict:
        query = """
                UNWIND $entity_id_set as entity_id 
                MATCH (node:Location{entityID: entity_id})
                WITH collect(node) as nodes
                CALL apoc.refactor.mergeNodes(nodes, 
                        {properties: {entityID: "discard", name:"combine", des:"combine"},
                        mergeRels:True})
                YIELD node 
                RETURN node.entityID as entityID, node.name as name, node.des as description
                """
        result = dao.run_write_query(query, {"entity_id_set": list(set(set_entity_id))}).data()
        return result


