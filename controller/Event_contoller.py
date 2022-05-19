from service.Event_Service import EventService
# Create SSE Server

class EventController:

    def __init__(self, sse):
        self.service = EventService()
        self.sse = sse

    def publish_message(self, element, action, json, type, channel):
        self.service.set_element(element)
        self.service.set_action(action)
        self.service.set_json(json)
        self.service.set_type(type)
        self.service.set_channel(channel)
        self.service.publish_service(self.sse)

    