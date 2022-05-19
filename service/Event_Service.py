

# Generate Events in this service

class EventService:
    def __init__(self):
        self.element = None
        self.action = None
        self.json = None
        self.channel = None
        self.type = None
    
    def publish_service(self,sse):
        sse.publish(self.element + ";" + self.action + ";" + self.json, type=self.type, channel=self.channel)

    def set_element(self, element):
        self.element = element

    def get_element(self):
        return self.element
    
    def set_action(self, action):
        self.action = action

    def get_action(self):
        return self.action

    def set_json(self, json):
        self.json = json

    def get_json(self):
        return self.json

    def set_type(self, type):
        self.type = type

    def get_type(self):
        return self.type

    def set_channel(self, channel):
        self.channel = channel

    def get_channel(self):
        return self.channel