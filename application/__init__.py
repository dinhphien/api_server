from application import settings
from application.utilities.data_access_object import DataAccessObject



dao = DataAccessObject(host=settings.NEO4J_HOST, port=settings.NEO4J_PORT,
                       user=settings.NEO4J_USER, password=settings.NEO4J_PASSWORD, scheme=settings.NEO4J_SCHEME)







