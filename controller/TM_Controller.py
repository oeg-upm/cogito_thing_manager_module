import json
import uuid

class TM_Controller:
    def __init__(self, id, request, event_controller):
        self.id = id
        self.request = request
        self.json_data = None
        self.event_controller = event_controller
        self.valid_id = self.is_valid_uuid(id)
        self.response = None

    def is_valid_uuid(self, value):
        try:
            uuid.UUID(value, version=4)
            return True
        except:
            return False

    def get_project(self):
        pass


    def project_definition(self, action):
        self.json_data = self.request.get_json()
        self.json_data.update({"id": self.id})
        self.event_controller.publish_message("project",
                                                action,
                                                json.dumps(self.json_data),
                                                "publish",
                                                "project")
        # Wrapper Execution

    def delete_project(self):
        # Call Triple Store Controller
        # Call Thing Directory Controller
        pass

    def add_file(self, action):
        self.json_data = self.request.get_json()
        # Analyse here what file format is the file uploaded
        # If json is a file list
        if isinstance(self.json_data, list):
            for file in self.json_data:
                file.update({"id": self.id})
                self.file_type_analysis(file, action)
                
        # If json is not a file list
        else:
            self.json_data.update({"id": self.id})
            self.file_type_analysis(self.json_data, action)

    def file_type_analysis(self, file, action):
        channel = self.event_controller.retrieve_channel(file["type"])
        if channel != "error":
            self.event_controller.publish_message("file",
                                                    action,
                                                    json.dumps(file),
                                                    "publish",
                                                    channel)
        else:
            self.response = "File type not supported: " + file["type"]
            self.event_controller.publish_message("file",
                                                    action,
                                                    json.dumps({
                                                        "Error" : "File type not supported",
                                                        "file_type" : file["type"]
                                                    }),
                                                    "publish",
                                                    channel)

    def delete_file_from_project(self):
        # Call Triple Store Controller
        # Call Thing Directory Controller
        pass

    def process_project_ttl(self):
        # Call Triple Store Controller
        # Call TD Service
        # Call Thing Directory Controller
        pass

    def process_file_ttl(self):
        # Call Triple Store Controller
        # Call TD Service
        # Call Thing Directory Controller
        pass
