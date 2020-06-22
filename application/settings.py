from environs import Env
env = Env()


DEBUG = env.bool('DEBUG', default=False)
BIND_HOST = env('BIND_HOST', default='0.0.0.0')
BIND_PORT = env.int('BIND_PORT', default=8888)

NEO4J_HOST = env('NEO4J_HOST', default='127.0.0.1')
NEO4J_PORT = env.int('NEO4J_PORT', default=7687)

NEO4J_USER = env('NEO4J_USER', default='neo4j')
NEO4J_PASSWORD = env('NEO4J_PASSWORD', default='neo4j')
NEO4J_SCHEME = env('NEO4J_SCHEME', default='bolt+routing')

SECRET_KEY = env("SECRET_KEY", "I'm Ron Burgundy?")
START_PAGIN = env.int('START_PAGIN', default=0)
LIMIT_PAGIN = env.int('LIMIT_PAGIN', default=1000)
LIMIT_NEWS =  env.int('LIMIT_NEWS', default=1000)