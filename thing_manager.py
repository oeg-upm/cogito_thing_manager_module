from TMConfiguration import TMConfiguration
from flask import Flask, json, send_file, request, make_response, jsonify, after_this_request, Response
from configparser import ConfigParser
from flask_sse import sse
from apscheduler.schedulers.background import BackgroundScheduler
from controller.Event_contoller import EventController
from controller.TM_Controller import TM_Controller
from controller.Error_Controller import Error_Controller
from controller.WoT_Hive_Controller import WoT_Hive_Controller
from controller.TD_Generator_Controller import TD_Generator_Controller
from controller.TripleStore_Controller import TripleStore_Controller
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
    tdd = WoT_Hive_Controller()
    if not tdd.get_td(id):
        if controller.valid_id:
            controller.project_definition(action="create")
            return "Created project with id: " + id
        else:
            error_controller = Error_Controller(id, "project", "create", "Invalid id, the id must be a valid uuid", event_controller)
            error_controller.publish_error()
            return "Invalid id, the id must be a valid uuid"
    else:
        return "Project already exists"


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
    #print(str(request.data))
    ttl = request.data.decode('utf-8')
    #print(ttl)
    ts_controller = TripleStore_Controller(ttl, id)
    ts_controller.serialize_graph()
    ts_controller.create_graph()
    td_controller = TD_Generator_Controller(id, "project", hierarchy_level=0, graph_data=ttl)
    td_controller.main()
    #print(td_controller.td)
    wot_controller = WoT_Hive_Controller()
    wot_controller.post_td(id, td_controller.td)
    return td_controller.td

@app.route("/project/<id>/<file_type>/<file_id>/ttl", methods=['POST'])
def process_file_ttl(id, file_type, file_id):
    """
    Retrieves from KGG the respective ttl file generated, saves it into the triple store and also generate respective thing descriptions for specific elements of the graph
    """
    ttl = request.data.decode('utf-8')
    file_url = ttl.split("\n")[-1]
    ttl = ttl.replace(file_url, "")
    file_url_td = {
            'FileStorage' : {
                'forms' : [
                    {
                        'href' : file_url,
                        'type' : file_type
                    }
                ]
            }
        }
    ts_controller = TripleStore_Controller(ttl, id, file_id)
    ts_controller.serialize_graph()
    ts_controller.create_graph()
    link_def = {
        "rel" : "",
        "href" : "",
        "type" : "application/td+json"
    }
    if file_type == "ifc":
        # file thing description
        td_controller = TD_Generator_Controller(id, "ifc", hierarchy_level=1, graph_data=ttl, file_id=file_id)
        td_controller.main()
        #print(td_controller.td)
        wot_controller = WoT_Hive_Controller()
        wot_controller.post_td(id, td_controller.td)
        # elements thing description
        td_controller = TD_Generator_Controller(id, "ifc", hierarchy_level=2, graph_data=ttl, file_id=file_id)
        td_controller.main()
        # Update with file storage information
        td_controller.td['properties'].update(file_url_td)
        # Update parent Thing Description
        link_def["rel"] = "facility:has" + file_type.capitalize()
        link_def["href"] = "http://data.cogito.iot.linkeddata.es/api/things/" + file_id
        wot_controller.update_td(id, link_def)
        #print(td_controller.thing_descriptions)
        for td in td_controller.thing_descriptions:
            td['properties'].update(file_url_td)
            wot_controller.post_td(id, td)
    else:
        #ttl = request.data.decode('utf-8')
        #print(ttl)
        ts_controller = TripleStore_Controller(ttl, id)
        ts_controller.serialize_graph()
        ts_controller.create_graph()
        td_controller = TD_Generator_Controller(id, file_type, hierarchy_level=1, graph_data=ttl, file_id=file_id)
        td_controller.main()
        td_controller.td['properties'].update(file_url_td)
        #print(td_controller.td)
        wot_controller = WoT_Hive_Controller()
        wot_controller.post_td(id, td_controller.td)
        # Update parent Thing Description
        link_def["rel"] = "facility:has" + file_type.capitalize()
        link_def["href"] = "http://data.cogito.iot.linkeddata.es/api/things/" + file_id
        wot_controller.update_td(id, link_def)

    return "TTL file retrieved with id: " + id + "\n file_type: " + file_type + "\n file_id: " + file_id + "\n thing description: \n" + str(td_controller.td)

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