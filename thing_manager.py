from TMConfiguration import TMConfiguration
from flask import Flask, json, send_file, request, make_response, jsonify, after_this_request, Response
from configparser import ConfigParser
from flask_sse import sse
from apscheduler.schedulers.background import BackgroundScheduler
from controller.Event_contoller import EventController
from controller.TM_Controller import TM_Controller
from controller.Error_Controller import Error_Controller
import sys
sys.stdout.flush()


app = Flask(__name__)
app.config["REDIS_URL"] = "redis://localhost:6379"
app.register_blueprint(sse, url_prefix='/stream')

@app.route("/project/<id>", methods=['GET'])
def get_project(id):
    """
    Retrieves the thing description of an existing project	
    """
    return "Get project with id: " + id

@app.route("/project/<id>", methods=['POST'])
def create_project(id):
    """
    Creates a new project, its respective triples and thing description, comes with a json file format
    """
    event_controller = EventController(sse)
    controller = TM_Controller(id, request, event_controller)
    if controller.valid_id:
        controller.project_definition(action="create")
        return "Created project with id: " + id
    else:
        error_controller = Error_Controller(id, "project", "create", "Invalid id, the id must be a valid uuid", event_controller)
        error_controller.publish_error()
        return "Invalid id, the id must be a valid uuid"

@app.route("/project/<id>", methods=['PUT'])
def update_project(id):
    """
    Updates an existing project, its respective triples and thing description
    """
    event_controller = EventController(sse)
    controller = TM_Controller(id, request, event_controller)
    if controller.valid_id:
        controller.project_definition(action="update")
        # execute update? --> carry action from wrapper to TM again and then handle with another service, like post or put?
        return "Updated project with id: " + id
    else:
        return "Invalid id, the id must be a valid uuid"

@app.route("/project/<id>", methods=['DELETE'])
def delete_project(id):
    """
    Deletes an existing project, its respective triples and thing description, and also the thing descriptions associated to it in cascade mode
    """
    return "Delete project with id: " + id

@app.route("/project/<id>/file", methods=['POST'])
def add_file_to_project(id):
    """
    Adds a file/files to an existing project, creates respective triples and thing descriptions (Creates one event per file)
    """
    event_controller = EventController(sse)
    controller = TM_Controller(id, request, event_controller)
    if controller.valid_id:
        controller.add_file(action="file_addition")
        if controller.response is not None:
            return controller.response
        else:
            return "Added file/s to project with id: " + id
    else:
        return "Invalid id, the id must be a valid uuid"

@app.route("/project/<id>/file", methods=['DELETE'])
def delete_file_from_project(id):
    """
    Deletes file from project and its respective triples and thing descriptions
    """
    return "Delete file from project with id: " + id

@app.route("/project/<id>/ttl", methods=['POST'])
def process_project_ttl(id):
    """
    Retrieves from KGG the respective ttl project file generated, saves it into the triple store and also generate respective thing description
    """
    print(str(request.data))
    return "Process project ttl with id: " + id

@app.route("/project/<id>/<file_type>/<file_id>/ttl", methods=['POST'])
def process_file_ttl(id, file_type, file_id):
    """
    Retrieves from KGG the respective ttl file generated, saves it into the triple store and also generate respective thing descriptions for specific elements of the graph
    """
    print(str(request.data))
    return "TTL file retrieved with id: " + id + "\n file_type: " + file_type + "\n file_id: " + file_id

@app.route("/project/<id>/wrapper_error", methods=['POST'])
def process_wrapper_error(id):
    """
    Handle wrapper error ocurred during the process of wrapper execution (json format)
    """
    print(str(request.data))
    #return "Wrapper error ocurred in project with id: " + id
    return request.data


#Example of a route for sse events publisher
# @app.route('/send')
# def send_message():
#     """
#     Send message to the client
#     """
#     controller = EventController(sse)
#     controller.publish_message("project","created","{'hello':'world'}", "publish", "analytics")
#     return "Message sent"


if __name__ == '__main__':

    config = ConfigParser()
    if config.read('./config.ini'):

        if not config.has_section('wot_directory'):
            print("Missing 'wot_directory' mandatory section in 'config.ini'.")
            exit()
        else:
            if not config.has_option('wot_directory', 'host'):
                print("Missing 'host' option in 'wot_directory' section in 'config.ini'.")
                exit()
        if not config.has_section('triple_store'):
            print("Missing 'triple_store' mandatory section in 'config.ini'.")
            exit()
        else:
            if not config.has_option('triple_store', 'host'):
                print("Missing 'host' option in 'triple_store' section in 'config.ini'.")
                exit()
            if not config.has_option('triple_store', 'user'):
                print("Missing 'user' option in 'triple_store' section in 'config.ini'.")
                exit()
            if not config.has_option('triple_store', 'password'):
                print("Missing 'password' option in 'triple_store' section in 'config.ini'.")
                exit()
        if not config.has_section('thing_manager'):
            print("Missing 'thing_manager' mandatory section in 'config.ini'.")
            exit()
        else:
            if not config.has_option('thing_manager', 'host'):
                print("Missing 'host' option in 'thing_manager' section in 'config.ini'.")
                exit()
            if not config.has_option('thing_manager', 'port'):
                print("Missing 'port' option in 'thing_manager' section in 'config.ini'.")
                exit()
        
        TMConfiguration.wot_directory = config.get('wot_directory', 'host')
        TMConfiguration.triple_store_host = config.get('triple_store', 'host')
        TMConfiguration.triple_store_user = config.get('triple_store', 'user')
        TMConfiguration.triple_store_password = config.get('triple_store', 'password')
        TMConfiguration.thing_manager_host = config.get('thing_manager', 'host')
        TMConfiguration.thing_manager_port = config.getint('thing_manager', 'port')
    else:
        print('Error reading config file.')

    app.run(debug=True, host=TMConfiguration.thing_manager_host, port=TMConfiguration.thing_manager_port)