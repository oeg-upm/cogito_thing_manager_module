import json


class TM_Controller:
    def __init__(self, id, request, event_controller):
        self.id = id
        self.request = request
        self.json_data = None
        self.event_controller = event_controller
        self.response = None

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
        if file["type"] == "ifc":
            self.event_controller.publish_message("file",
                                                    action,
                                                    json.dumps(file),
                                                    "publish",
                                                    "file.ifc")
        elif file["type"] == "schedule":
            self.event_controller.publish_message("file",
                                                    action,
                                                    json.dumps(file),
                                                    "publish",
                                                    "file.schedule")
        elif file["type"] == "visual_qc":
            self.event_controller.publish_message("file",
                                                    action,
                                                    json.dumps(file),
                                                    "publish",
                                                    "file.visual_qc")
        else:
            self.response = "File type not supported: " + file["type"]
            self.event_controller.publish_message("file",
                                                    action,
                                                    json.dumps({
                                                        "Error" : "File type not supported",
                                                        "file_type" : file["type"]
                                                    }),
                                                    "publish",
                                                    "error")

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
