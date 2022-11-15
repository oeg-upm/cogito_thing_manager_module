

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
            "in_process": [{
                    "project_id": "123",
                    "file_id": "456",
                    "file_type": "schedule",
                    "in_progress": True,
                    "timestamp": "01-01-2020, 00:00:00",
                    "error_message": None
                },
                {
                    "project_id": "2",
                    "file_id": None,
                },
                {
                    "project_id": "3",
                    "file_id": None,
                }],
            "completed": [],
            "error": []
        }

    def update_json(self, event_json):
        self.event_json = event_json