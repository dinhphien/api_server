from application import dao
from typing import List, Dict
from application.utilities.graph import serialize_node_to_dict

class EventService:
    @staticmethod
    def get_all(start=0, limit=100) -> List:
        query = """
        MATCH (event:Event)
        RETURN event.entityID as entityID, event.name as name, event.des as description
        ORDER BY event.entityID
        SKIP $start
        LIMIT $limit
        """
        return dao.run_read_query(query, start=start, limit=limit).data()

    @staticmethod
    def get_by_id(event_id):
        query = """
        MATCH (event:Event{entityID: $event_id}) 
        RETURN event.entityID as entityID, event.name as name, event.des as description
        """
        return dao.run_read_query(query, event_id=event_id).data()

    @staticmethod
    def create(event_properties):
        query = """
        CREATE (event:Event $props)
        RETURN event.entityID as entityID, event.name as name, event.des as description
        """
        return dao.run_write_query(query, props= event_properties).data()

    @staticmethod
    def update(event_properties: Dict, event_id: str):
        query = """
            MATCH (event:Event{entityID: $id_event})
            SET event = $props
            RETURN event.entityID as entityID, event.name as name, event.des as description
            """
        return dao.run_write_query(query, {"props":event_properties, "id_event": event_id}).data()

    @staticmethod
    def is_in_news(event_id) -> bool:
        query = """
        MATCH (fact:Fact)-[]->(:Event{entityID: $id_entity})
        RETURN count(fact) as numAppearance
        """
        result = dao.run_read_query(query, id_entity=event_id).data()
        if result[0]["numAppearance"] == 0:
            return False
        else:
            return True

    @staticmethod
    def delete(event_id):
        query = """
        MATCH (event: Event{entityID: $id_entity})
        DELETE event
        """
        return dao.run_write_query(query, id_entity=event_id).data()

    @staticmethod
    def search(start=0, limit=100, *args, **kwargs):
        text_search = args[0]
        query = "CALL db.index.fulltext.queryNodes(" + "'eventsFullTextSearch', '" + text_search + \
                "') YIELD node, score  RETURN node.entityID as entityID, node.name as name," \
                "node.des as description, score ORDER BY score DESC"
        return dao.run_read_query(query).data()[start:start+limit]

    @staticmethod
    def merge_nodes(set_entity_id: List[str]) -> Dict:
        query = """
                UNWIND $entity_id_set as entity_id 
                MATCH (node:Event{entityID: entity_id})
                WITH collect(node) as nodes
                CALL apoc.refactor.mergeNodes(nodes, 
                        {properties: {entityID: "discard", name:"combine", des:"combine"},
                        mergeRels:True})
                YIELD node 
                RETURN node.entityID as entityID, node.name as name, node.des as description
                """
        result = dao.run_write_query(query, {"entity_id_set": list(set(set_entity_id))}).data()
        return result


