import json
import uuid

class Error_Controller:
    def __init__(self, id, element, action, description, event_controller):
        self.element = element
        self.action = action
        self.description = description + " - ProjectID:" + str(id)
        self.event_controller = event_controller

    def publish_error(self):
        self.event_controller.publish_message("element",
                                                self.action,
                                                self.description,
                                                "publish",
                                                "errors")