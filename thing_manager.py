from TMConfiguration import TMConfiguration
from service.Error_Handling_Service import Error_Handling_Service
from flask import Flask, json, send_file, request, make_response, jsonify, after_this_request, Response
from configparser import ConfigParser
from flask_sse import sse
from apscheduler.schedulers.background import BackgroundScheduler
from controller.Event_contoller import EventController
from controller.TM_Controller import TM_Controller
from service.Error_Handling_Service import Error_Handling_Service
from controller.WoT_Hive_Controller import WoT_Hive_Controller
from controller.TD_Generator_Controller import TD_Generator_Controller
from controller.TripleStore_Controller import TripleStore_Controller
from controller.Coppola_Controller import Coppola_Controller
import os
import sys
import hashlib
sys.stdout.flush()


app = Flask(__name__)
# app.config["REDIS_URL"] = "redis://localhost:6379"
app.config['REDIS_URL'] = os.getenv('REDIS_URL')
print("Redis Host: ", os.getenv('REDIS_URL'))
app.register_blueprint(sse, url_prefix='/stream')


@app.route("/status", methods=['GET','POST']) # if method GET --> return get all entries else read json and get specific entry
def get_status():
    """
    Retrieves the thing description of an existing project	-- This function can be done by asking the WoT-Hive
    """
    if request.method == 'GET':
        return error_service.get_all_entries()
    elif request.method == 'POST':
        if "project_id" in request.json:
            project_id = request.json["project_id"]
        else:
            return "Project ID not provided"
        if "file_id" in request.json:
            file_id = request.json["file_id"]
        else:
            file_id = None
        return error_service.get_entry(project_id, file_id)
    else:
        return "Method not allowed", 405

@app.route("/project/<id>", methods=['POST'])
def create_project(id):
    """
    Creates a new project, its respective triples and thing description, comes with a json file format
    """
    if request.method == 'POST':
        event_controller = EventController(sse)
        controller = TM_Controller(id, request, event_controller)
        tdd = WoT_Hive_Controller(TMConfiguration.wot_directory)
        if not tdd.get_td(id):
            if controller.valid_id:
                controller.project_definition(action="create")
                error_service.create_entry(event = "in_process", project_id = id, in_progress = True, file_id = None, error_message = None, wrapper = False)
                return "Project " + id + " creation in progress."
            else:
                return "Invalid id, the id must be a valid uuid"
        else:
            return "Project already exists!"
    else:
        return "Method not allowed", 405

@app.route("/project/<id>", methods=['DELETE'])
def delete_project(id):
    """
    Deletes an existing project, its respective triples and thing description, and also the thing descriptions associated to it in cascade mode
    NO PROJECTS WILL BE DELETED
    """
    if request.method == 'DELETE':
        try:
            ts_controller = TripleStore_Controller(None, id, TMConfiguration.triple_store_host, TMConfiguration.triple_store_user, TMConfiguration.triple_store_password)
            ts_controller.delete_graph()
            tdd = WoT_Hive_Controller(TMConfiguration.wot_directory)
            td = tdd.get_td(id).json()
            if td['types'] == "https://cogito.iot.linkeddata.es/def/facility#Project":
                if td["links"] != []:
                    for link in td["links"]:
                        tdd.delete_td(link["href"].replace("http://data.cogito.iot.linkeddata.es/api/things/", ""))
                tdd.delete_td(id)
            return "Delete project with id: " + id + " and all its associated thing descriptions."
        except:
            return "Project " + id + " does not exist."
    else:
        return "Method not allowed", 405

@app.route("/project/<id>/file", methods=['POST'])
def add_file_to_project(id):
    """
    Adds a file/files to an existing project, creates respective triples and thing descriptions (Creates one event per file)
    """
    if request.method == 'POST':
        event_controller = EventController(sse)
        controller = TM_Controller(id, request, event_controller)
        tdd = WoT_Hive_Controller(TMConfiguration.wot_directory)
        if tdd.get_td(id):
            if controller.valid_id:
                controller.add_file(action="file_addition")
                if controller.response is not None:
                    return controller.response
                else:
                    file_id = hashlib.sha256(request.json["file_url"].encode('utf-8')).hexdigest()
                    file_type = request.json["type"]
                    error_service.create_entry(event = "in_process", project_id = id, in_progress = True, file_id = file_id, file_type = file_type, error_message = None, wrapper = False)
                    return "Addition of file/s to project with id: " + id + " in progress."
            else:
                return "Invalid id, the id must be a valid uuid"
        else:
            return "Project with id:" + id + " does not exist!"
    else:
        return "Method not allowed", 405

@app.route("/project/<id>/file/<file_id>", methods=['DELETE'])
def delete_file_from_project(id, file_id):
    """
    Deletes file from project and its respective triples and thing descriptions
    Update parent project thing description removing the td link from links
    """
    if request.method == 'DELETE':
        try:
            ts_controller = TripleStore_Controller(None, id, TMConfiguration.triple_store_host, TMConfiguration.triple_store_user, TMConfiguration.triple_store_password, file_id=file_id)
            ts_controller.delete_graph()
            tdd = WoT_Hive_Controller(TMConfiguration.wot_directory)
            td = tdd.get_td(id).json()
            if td['types'] == "https://cogito.iot.linkeddata.es/def/facility#Project":
                if td["links"] != []:
                    for link in td["links"]:
                        if link["href"] ==  "http://data.cogito.iot.linkeddata.es/api/things/" + file_id:
                            td["links"].remove(link)
            tdd.post_td(id, td)
            tdd.delete_td(file_id)
            return "Delete file with id: " + file_id + " and related thing descriptions from project with id: " + id
        except:
            return "File " + file_id + " does not exist in project " + id + "."
    else:
        return "Method not allowed", 405

@app.route("/project/<id>/ttl", methods=['POST'])
def process_project_ttl(id):
    """
    Retrieves from KGG the respective ttl project file generated, saves it into the triple store and also generate respective thing description
    """
    if request.method == 'POST':
        ttl = request.data.decode('utf-8')
        try:
            ts_controller = TripleStore_Controller(ttl, id, TMConfiguration.triple_store_host, TMConfiguration.triple_store_user, TMConfiguration.triple_store_password)
            ts_controller.serialize_graph()
            ts_controller.create_graph()
        except:
            error_service.create_entry(event = "error", project_id = id, in_progress = False, file_id = None, file_type = None, error_message = "Error saving Knowledge Graph in Triplestore", wrapper = False)
        try:
            td_controller = TD_Generator_Controller(id, "project", hierarchy_level=0, graph_data=ttl)
            td_controller.main()
        except:
            error_service.create_entry(event = "error", project_id = id, in_progress = False, file_id = None, file_type = None, error_message = "Error generating Thing Description", wrapper = False)
        try:
            wot_controller = WoT_Hive_Controller(TMConfiguration.wot_directory)
            wot_controller.post_td(id, td_controller.td)
            error_service.create_entry(event = "completed", project_id = id, in_progress = False, file_id = None, file_type = None, error_message = None, wrapper = False)
        except:
            error_service.create_entry(event = "error", project_id = id, in_progress = False, file_id = None, file_type = None, error_message = "Error saving Thing Description in WoT Hive", wrapper = False)
        return td_controller.td
    else:
        return "Method not allowed", 405

@app.route("/project/<id>/<file_type>/<file_id>/ttl", methods=['POST'])
def process_file_ttl(id, file_type, file_id):
    """
    Retrieves from KGG the respective ttl file generated, saves it into the triple store and also generate respective thing descriptions for specific elements of the graph
    """
    if request.method == 'POST':
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

        if file_type == "iot" or file_type == "vqc" or file_type == "gqc":
            # Triple Store validate graph
            validation_controller = Coppola_Controller(ttl)
            validation_controller.validate()
            if validation_controller.validation_error == True:
                return "Error validating"
            # if some of the elements of the list of validation response contains a conforms == false, return error, ttl malformed.
            # Triple Store save graph
            #ts_controller = TripleStore_Controller(ttl, id, TMConfiguration.triple_store_host, TMConfiguration.triple_store_user, TMConfiguration.triple_store_password, file_id=file_id)
            #ts_controller.serialize_graph()
            #ts_controller.create_graph()
            
            # TD Generator Controller
            
            pass
        else:
            # Triple Store save graph
            try:
                ts_controller = TripleStore_Controller(ttl, id, TMConfiguration.triple_store_host, TMConfiguration.triple_store_user, TMConfiguration.triple_store_password, file_id=file_id)
                ts_controller.serialize_graph()
                ts_controller.create_graph()
            except:
                error_service.create_entry(event = "error", project_id = id, in_progress = False, file_id = file_id, file_type = file_type, error_message = "Error saving Knowledge Graph in Triplestore", wrapper = False)

            link_def = {
                "rel" : "",
                "href" : "",
                "type" : "application/td+json"
            }
            if file_type == "ifc":
                # file thing description
                try:
                    td_controller = TD_Generator_Controller(id, "ifc", hierarchy_level=1, graph_data=ttl, file_id=file_id)
                    td_controller.main()
                except:
                    error_service.create_entry(event = "error", project_id = id, in_progress = False, file_id = file_id, file_type = file_type, error_message = "Error generating Thing Description of ifc file.", wrapper = False)
                try:
                    wot_controller = WoT_Hive_Controller(TMConfiguration.wot_directory)
                    wot_controller.post_td(td_controller.td["id"], td_controller.td)
                except:
                    error_service.create_entry(event = "error", project_id = id, in_progress = False, file_id = file_id, file_type = file_type, error_message = "Error saving Thing Description in WoT Hive ifc file information.", wrapper = False)
                # elements thing description
                try:
                    td_controller = TD_Generator_Controller(id, "ifc_elements", hierarchy_level=2, graph_data=ttl, file_id=file_id)
                    td_controller.main()
                    # Update with file storage information
                    td_controller.td['properties'].update(file_url_td)
                    # Update parent Thing Description
                    link_def["rel"] = "facility:has" + file_type.capitalize()
                    link_def["href"] = "http://data.cogito.iot.linkeddata.es/api/things/" + file_id
                    parent_td = td_controller.td

                    r = wot_controller.get_td(id)
                    if r.status_code != 404:
                        return "Error Project ID not found"
                    else:
                        try:
                            wot_controller.predetermined_td_set(id)
                            wot_controller.post_td(id, wot_controller.predetermined_td)
                            wot_controller.update_td(id, link_def)
                        except:
                            error_service.create_entry(event = "error", project_id = id, in_progress = False, file_id = file_id, file_type = file_type, error_message = "Error updating Thing Description in WoT Hive project information.", wrapper = False)

                    try:
                        for td in td_controller.thing_descriptions:
                            td['properties'].update(file_url_td)
                            wot_controller.post_td(td["id"], td)
                        error_service.create_entry(event = "completed", project_id = id, in_progress = False, file_id = file_id, file_type = file_type, error_message = None, wrapper = False)
                        return parent_td
                    except:
                        error_service.create_entry(event = "error", project_id = id, in_progress = False, file_id = file_id, file_type = file_type, error_message = "Error saving Thing Descriptions of elements information in WoT Hive.", wrapper = False)
                except:
                    error_service.create_entry(event = "error", project_id = id, in_progress = False, file_id = file_id, file_type = file_type, error_message = "Error generating Thing Description of ifc elements.", wrapper = False)
            
            else:
                try:
                    td_controller = TD_Generator_Controller(id, file_type, hierarchy_level=1, graph_data=ttl, file_id=file_id)
                    td_controller.main()
                    td_controller.td['properties'].update(file_url_td)
                except:
                    error_service.create_entry(event = "error", project_id = id, in_progress = False, file_id = file_id, file_type = file_type, error_message = "Error generating Thing Description of " + file_type + " file.", wrapper = False)
                try:
                    wot_controller = WoT_Hive_Controller(TMConfiguration.wot_directory)
                    wot_controller.post_td(td_controller.td["id"], td_controller.td)
                    # Update parent Thing Description
                    link_def["rel"] = "facility:has" + file_type.capitalize()
                    link_def["href"] = "http://data.cogito.iot.linkeddata.es/api/things/" + file_id
                    parent_td = td_controller.td

                    r = wot_controller.get_td(id)
                    if r.status_code != 404:
                        wot_controller.update_td(id, link_def)
                    else:
                        wot_controller.predetermined_td_set(id)
                        wot_controller.post_td(id, wot_controller.predetermined_td)
                        wot_controller.update_td(id, link_def)
                    
                    error_service.create_entry(event = "completed", project_id = id, in_progress = False, file_id = file_id, file_type = file_type, error_message = None, wrapper = False)
                    return parent_td
                except:
                    error_service.create_entry(event = "error", project_id = id, in_progress = False, file_id = file_id, file_type = file_type, error_message = "Error saving Thing Description " + file_type + " file information in WoT Hive.", wrapper = False)
    else:
        return "Method not allowed", 405

@app.route("/wrapper_error", methods=['POST'])
def process_wrapper_error():
    """
    Handle wrapper error ocurred during the process of wrapper execution (json format)
    """
    if request.method == 'POST':
        print("In Wrapper Error")
        json_error = request.json
        error_service.create_entry(event = "error", project_id = json_error["project_id"], in_progress = False, file_id = json_error["file_id"], error_message = json_error["error"], wrapper = True)
        return "Error Registered"
    else:
        return "Method not allowed", 405
    


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
        if not config.has_section('coppola'):
                print("Missing 'coppola' mandatory section in 'config.ini'.")
                exit()
        else:
            if not config.has_option('coppola', 'host'):
                print("Missing 'host' option in 'coppola' section in 'config.ini'.")
                exit()
        
        TMConfiguration.wot_directory = config.get('wot_directory', 'host')
        TMConfiguration.triple_store_host = config.get('triple_store', 'host')
        TMConfiguration.triple_store_user = config.get('triple_store', 'user')
        TMConfiguration.triple_store_password = config.get('triple_store', 'password')
        TMConfiguration.thing_manager_host = config.get('thing_manager', 'host')
        TMConfiguration.thing_manager_port = config.getint('thing_manager', 'port')
        TMConfiguration.coppola = config.get('coppola', 'host')
    else:
        print('Error reading config file.')

    error_service = Error_Handling_Service()
    error_service.init_json()
    app.run(debug=True, host=TMConfiguration.thing_manager_host, port=TMConfiguration.thing_manager_port)