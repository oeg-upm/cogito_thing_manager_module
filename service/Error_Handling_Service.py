import datetime
from model.Errors import Errors

class Error_Handling_Service:
    def __init__(self):
        self.entry = None
        self.error_model = Errors()
        self.event_listener_json = None

    def init_json(self):
        self.error_model.init_json()

    def init_service(self):
        self.event_listener_json = self.error_model.get_json()

    def json_template(self):
        dictionary = {
            "project_id": None,
            "file_id": None,
            "file_type": None,
            "in_progress": False,
            "timestamp": None,
            "error_message": None
        }
        return dictionary

    def fill_json(self, project_id, file_id, file_type, in_progress, error_message = None):
        self.entry = self.json_template()
        self.entry["project_id"] = project_id
        self.entry["file_id"] = file_id
        self.entry["file_type"] = file_type
        self.entry["in_progress"] = in_progress
        self.entry["timestamp"] = datetime.datetime.now().strftime("%d-%m-%Y, %H:%M:%S")
        self.entry["error_message"] = error_message
        


    def create_entry(self, event, project_id, in_progress, file_id = None, file_type = None, error_message = None, wrapper = False):
        self.init_service()
        # analyze entries identifies if the event is in progress, completed, or error
        r = self.analyze_entries(project_id, file_id)
        # if exists delete
        if wrapper and r != []:
            file_type = self.get_entry(project_id, file_id)["file_type"]
        if r != []:
            [self.delete_entry(elem, project_id, file_id) for elem in r]
        # create entry
        self.fill_json(project_id, file_id, file_type, in_progress, error_message)
        self.event_listener_json[event].append(self.entry)
        self.error_model.update_json(self.event_listener_json)
        self.entry = None
        

    def delete_entry(self, event, project_id, file_id = None): # event can be in_process, completed, error
        self.init_service()
        if file_id != None:
            [self.event_listener_json[event].pop(self.event_listener_json[event].index(elem)) for elem in self.event_listener_json[event] if elem["project_id"] == project_id and elem["file_id"] == file_id]
        else:
            [self.event_listener_json[event].pop(self.event_listener_json[event].index(elem)) for elem in self.event_listener_json[event] if elem["project_id"] == project_id]
                

    def get_entry(self, project_id, file_id = None):
        self.init_service()
        r = self.analyze_entries(project_id, file_id)
        if r != []:
            for elem in self.event_listener_json[r[0]]:
                if file_id != None:
                    if elem["project_id"] == project_id and elem["file_id"] == file_id:
                        return elem
                else:
                    if elem["project_id"] == project_id:
                        return elem
        else:
            return "No entry found"

    def get_all_entries(self):
        self.init_service()
        return self.event_listener_json

    def get_all_entries_by_event(self, event):
        pass

    def analyze_entries(self, project_id, file_id = None):
        events = ["in_process", "completed", "error"]
        if file_id == None:
            res = [[event for elem in self.event_listener_json[event] if elem["project_id"] == project_id and self.event_listener_json[event] != []] for event in events]
        else:
            res = [[event for elem in self.event_listener_json[event] if elem["project_id"] == project_id and elem["file_id"] == file_id] for event in events]
        r = [r[0] for r in res if r != []]
        return r