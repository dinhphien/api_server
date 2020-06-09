from application import dao
from typing import List, Dict

class AuthService:
    @staticmethod
    def createUser(username, password, token):
        query = """
        CREATE (usr:User { username: $usr, password: $paswd, token: $token, isAdmin: $isAd })
        RETURN usr.username as username, usr.password as password, usr.token as token, usr.isAdmin as isAdmin
        """
        result =  dao.run_write_query(query, usr= username, paswd=password, token=token, isAd=False).data()
        res = result[0]
        res['token'] = res['token'].decode('utf-8')
        return res

    @staticmethod
    def createAdmin(username, password, token):
        query = """
        CREATE (usr:Admin { username: $usr, password: $paswd, token: $token, isAdmin: $isAd })
        RETURN usr.username as username, usr.password as password, usr.token as token, usr.isAdmin as isAdmin
        """
        result = dao.run_write_query(query, usr=username, paswd=password, token=token, isAd=True).data()
        res = result[0]
        res['token'] = res['token'].decode('utf-8')
        return res


    @staticmethod
    def checkAdminAccount(username, password):
        query = """
        MATCH (usr:Admin { username: $usr, password: $paswd })
        RETURN usr.username as username, usr.password as password, usr.token as token, usr.isAdmin as isAdmin
        """
        result = dao.run_read_query(query, usr=username, paswd= password).data()
        res = result[0]
        res['token'] = res['token'].decode('utf-8')
        return res



    @staticmethod
    def checkUserAccount(username, password):
        query = """
           MATCH (usr:User { username: $usr, password: $paswd })
           RETURN usr.username as username, usr.password as password, usr.token as token, usr.isAdmin as isAdmin
           """
        result = dao.run_read_query(query, usr=username, paswd=password).data()
        res = result[0]
        res['token'] = res['token'].decode('utf-8')
        return res


    @staticmethod
    def getUser(username):
        query = """
        MATCH (usr:User { username: $usr})
        RETURN usr.username as username, usr.password as password, usr.token as token, usr.isAdmin as isAdmin
        """
        return dao.run_read_query(query, usr=username).data()

    @staticmethod
    def getAdmin(username):
        query = """
        MATCH (usr:Admin { username: $usr})
        RETURN usr.username as username, usr.password as password, usr.token as token, usr.isAdmin as isAdmin
        """
        return dao.run_read_query(query, usr=username).data()

