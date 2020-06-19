from application import settings
from application.utilities.data_access_object import DataAccessObject
from neo4j import CypherError

dao = DataAccessObject(host=settings.NEO4J_HOST, port=settings.NEO4J_PORT,
                       user=settings.NEO4J_USER, password=settings.NEO4J_PASSWORD, scheme=settings.NEO4J_SCHEME)


def init_neo4j_database():
    array_query_index = {}
    array_query_index["news_index"] = """
    CREATE INDEX index_news FOR (news:News) ON (news.entityID)
    """
    array_query_index["agr_full_text"] = """
    CALL db.index.fulltext.createNodeIndex("agreementsFullTextSearch",["Agreement"],["name", "des"])
    """
    array_query_index["cty_full_text"] = """
    CALL db.index.fulltext.createNodeIndex("countriesFullTextSearch",["Country"],["name", "des"])
    """
    array_query_index["event_full_text"] = """
    CALL db.index.fulltext.createNodeIndex("eventsFullTextSearch",["Event"],["name", "des"])
    """
    array_query_index["loc_full_text"] = """
    CALL db.index.fulltext.createNodeIndex("locationsFullTextSearch",["Location"],["name", "des"])
    """
    array_query_index["org_full_text"] = """
    CALL db.index.fulltext.createNodeIndex("organizationsFullTextSearch",["Organization"],["name", "des"])
    """
    array_query_index["per_full_text"] = """
    CALL db.index.fulltext.createNodeIndex("personsFullTextSearch",["Person"],["name", "des"])
    """
    # create indexes:
    for key in array_query_index:
        query = array_query_index[key]
        try:
            result = dao.run_write_query(query).data()
        except CypherError:
            continue
    return 0

init_neo4j_database()





