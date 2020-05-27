from neo4j import GraphDatabase


class DataAccessObject:
    def __init__(self, host, port, user, password):
        uri = "neo4j://" + host + ":" + str(port)
        self._driver = GraphDatabase.driver(uri, auth=(user, password), encrypted=False)

    def close(self):
        self._driver.close()

    def run_read_query(self, query, params=None, **kwparams):
        with self._driver.session() as session:
            result = session.read_transaction(self.run_unit_of_work, query, params, **kwparams)
            return result

    def run_write_query(self, query, params=None, **kwparams):
        with self._driver.session() as session:
            result = session.write_transaction(self.run_unit_of_work, query, params, **kwparams)
            return result

    @staticmethod
    def run_unit_of_work(tx, query, params, **kwparams):
        return tx.run(query, params, **kwparams)


