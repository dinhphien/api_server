from application import dao
from typing import List, Dict

def convert_date_results_to_string(result: List)->List:
    converted_result = []
    for index in range(0, len(result)):
        record = result[index]
        if isinstance(record['description'], list):
            for i in range(0, len(record['description'])):
                record['description'][i] = record['description'][i].__str__()
        else:
            record['description'] = record['description'].__str__()
        converted_result.append(record)
    return converted_result



class TimeService:
    @staticmethod
    def get_all(start=0, limit=100) -> List:
        query = """
        MATCH (tim:Time)
        RETURN tim.entityID as entityID, tim.name as name, tim.des as description
        ORDER BY tim.entityID
        SKIP $start
        LIMIT $limit
        """
        result = dao.run_read_query(query, start= start, limit=limit).data()
        return convert_date_results_to_string(result)

    @staticmethod
    def get_by_id(tim_id):
        query = """
        MATCH (tim:Time{entityID: $tim_id}) 
        RETURN tim.entityID as entityID, tim.name as name, tim.des as description
        """
        result = dao.run_read_query(query, tim_id=tim_id).data()
        return convert_date_results_to_string(result)

    @staticmethod
    def create(time_properties):
        query = """
        CREATE (tim:Time $props)
        RETURN tim.entityID as entityID, tim.name as name, tim.des as description
        """
        result = dao.run_write_query(query, props= time_properties).data()
        return convert_date_results_to_string(result)

    @staticmethod
    def update(time_properties: Dict, tim_id: str):
        query = """
            MATCH (tim:Time{entityID: $id_tim})
            SET tim = $props
            RETURN tim.entityID as entityID, tim.name as name, tim.des as description
            """
        result =  dao.run_write_query(query, {"props":time_properties, "id_tim": tim_id}).data()
        return convert_date_results_to_string(result)

    @staticmethod
    def is_in_news(tim_id) -> bool:
        query = """
        MATCH (fact:Fact)-[]->(:Time{entityID: $id_entity})
        RETURN count(fact) as numAppearance
        """
        result = dao.run_read_query(query, id_entity=tim_id).data()
        if result[0]["numAppearance"] == 0:
            return False
        else:
            return True

    @staticmethod
    def delete(tim_id):
        query = """
        MATCH (tim: Time{entityID: $id_entity})
        DELETE tim
        """
        return dao.run_write_query(query, id_entity=tim_id).data()

    @staticmethod
    def search(start=0, limit=100, *args, **kwargs):

        query = """
            MATCH(entity:Time)
            WHERE entity.des CONTAINS $property OR entity.name CONTAINS $property
            RETURN entity.entityID as entityID, entity.name as name, entity.des as description
            ORDER BY entity.entityID
            SKIP $start
            LIMIT $limit
            """
        result =  dao.run_read_query(query, {"property": args[0], "start":start, "limit":limit}).data()
        return convert_date_results_to_string(result)

    @staticmethod
    def merge_nodes(set_entity_id: List[str]) -> Dict:
        query = """
                UNWIND $entity_id_set as entity_id 
                MATCH (node:Time{entityID: entity_id})
                WITH collect(node) as nodes
                CALL apoc.refactor.mergeNodes(nodes, 
                        {properties: {entityID: "discard", name:"combine", des:"combine"},
                        mergeRels:True})
                YIELD node 
                RETURN node.entityID as entityID, node.name as name, node.des as description
                """
        result = dao.run_write_query(query, {"entity_id_set": list(set(set_entity_id))}).data()
        return convert_date_results_to_string(result)


