from service.Event_Service import EventService
# Create SSE Server

class EventController:

    def __init__(self, sse):
        self.service = EventService()
        self.sse = sse
        self.json = {
            "@context": "https://www.w3.org/2019/wot/td/v1",
            "title": "Channel Thing Description",
            "id": "123456789",
            "description": "Channel Thing Description to retrieve channel for server sent events",
            "properties": {
                "Channels": {
                    "forms": [
                        {
                            "href": "file.ifc",
                            "type": "ifc"
                        },
                        {
                            "href": "file.schedule",
                            "type": "schedule"
                        },
                        {
                            "href": "file.res_types",
                            "type": "resource_types"
                        },
                        {
                            "href": "file.v_qc",
                            "type": "visual_qc"
                        }
                    ]
                }
            },
            "actions": {},
            "events": {},
            "links": [],
            "security": [
                "nosec_sc"
            ],
            "securityDefinitions": {
                "nosec_sc": {
                    "scheme": "nosec"
                }
            }
        }

    def publish_message(self, element, action, json, type, channel):
        self.service.set_element(element)
        self.service.set_action(action)
        self.service.set_json(json)
        self.service.set_type(type)
        self.service.set_channel(channel)
        self.service.publish_service(self.sse)

    def retrieve_channel(self, type):
        for elem in self.json["properties"]["Channels"]["forms"]:
            if elem["type"] == type:
                return elem["href"]
            # is element is last element in the list
            if elem == self.json["properties"]["Channels"]["forms"][-1]:
                return "error"