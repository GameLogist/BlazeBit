# import docker as dr
from flask import Blueprint
dockerpy = Blueprint('dockerpy', __name__)

def create_container():

    # client = dr.from_env()
    # client.containers.run('alpine', 'echo hello world', detach=True, remove=True)
    return "Hello World!"
