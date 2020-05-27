from environs import Env


env = Env()


DEBUG = env.bool('DEBUG', default=False)
BIND_HOST = env('BIND_HOST', default='127.0.0.1')
BIND_PORT = env.int('BIND_PORT', default=5000)
# BIND_HOST = env('DOCKER_HOST_IP', default='172.17.0.1')

NEO4J_HOST = env('NEO4J_HOST', default='127.0.0.1')
# NEO4J_HOST = env('DOCKER_HOST_IP', default='172.17.0.1')
NEO4J_PORT = env.int('NEO4J_PORT', default=7687)

NEO4J_USER = env('NEO4J_USER', default='neo4j')
NEO4J_PASSWORD = env('NEO4J_PASSWORD', default='xyzzy')