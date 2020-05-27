from neo4j import Relationship, Node
from typing import Dict
from itertools import chain





def serialize_node_to_dict(node: Node) -> Dict:

    result_node = {}

    if isinstance(node, Node):
        result_node["id"] = str(node["entityID"])
        result_node["labels"] = list(chain(node.labels))
        result_node["properties"] = dict(node)
        result_node["properties"].pop("entityID", None)

        if "Time" in result_node["labels"]:
            if not isinstance(result_node["properties"]["des"], list):
                result_node["properties"]["des"] = result_node["properties"]["des"].__str__()
            else:
                for index in range(0, len(result_node["properties"]["des"])):
                    result_node["properties"]["des"][index] = result_node["properties"]["des"][index].__str__()
    return result_node


def serialize_relation_to_dict(relation: Relationship) -> Dict:
    result_relation = {}
    if isinstance(relation, Relationship):
        result_relation["id"] = str(relation.id)
        result_relation["type"] = relation.type
        result_relation["startNode"] = str(relation.start_node["entityID"])
        result_relation["endNode"] = str(relation.end_node["entityID"])
        result_relation["properties"] = dict(relation)
    return result_relation


def serialize_subgraph_to_dict(graph) -> Dict :
    graph_format_result = {
        "results": [{
            "columns": [],
            "data": [{
                "graph": {
                    "nodes": [],
                    "relationships": [],
                },
            }],
        }],
        "errors": []
    }

    for node in graph.nodes:
        dict_node = serialize_node_to_dict(node)
        graph_format_result["results"][0]["data"][0]["graph"]["nodes"].append(dict_node)
    for relation in graph.relationships:
        dict_relation = serialize_relation_to_dict(relation)
        graph_format_result["results"][0]["data"][0]["graph"]["relationships"].append(dict_relation)

    return graph_format_result


