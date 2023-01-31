

class Errors:
    def __init__(self):
        self.event_json = None


    def get_json(self):
        return self.event_json

    def init_json(self):
        # self.event_json = {
        #     "in_process": [],
        #     "completed": [],
        #     "error": []
        # }
        self.event_json = {
            "in_process": [],
            "completed": [],
            "error": []
        }

    def update_json(self, event_json):
        self.event_json = event_json