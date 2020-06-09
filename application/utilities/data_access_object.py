from neo4j import GraphDatabase


class DataAccessObject:
    def __init__(self, host, port, user, password, scheme):
        uri = scheme + "://" + host + ":" + str(port)
        self._driver = GraphDatabase.driver(uri, auth=(user, password), encrypted=False)

    def close(self):
        self._driver.close()

    def run_read_query(self, query, params=None, **kwparams):
        result = self._driver.session().read_transaction(self.run_unit_of_work, query, params, **kwparams)
        return result

    def run_write_query(self, query, params=None, **kwparams):
        result = self._driver.session().write_transaction(self.run_unit_of_work, query, params, **kwparams)
        return result

    @staticmethod
    def run_unit_of_work(tx, query, params, **kwparams):
        return tx.run(query, params, **kwparams)