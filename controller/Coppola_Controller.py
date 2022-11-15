import requests
from TMConfiguration import TMConfiguration

class Coppola_Controller:
    def __init__(self, ttl, coppola_endpoint):
        self.coppola_endpoint = coppola_endpoint
        self.ttl = ttl
        self.url_list = None
        self.response_list = None
        self.shacl_shapes_path = [
            "./repository/shacl_shapes/facility-shapes.ttl",
            "./repository/shacl_shapes/process-shapes.ttl",
            "./repository/shacl_shapes/quality-shapes.ttl",
            "./repository/shacl_shapes/resource-shapes.ttl",
            "./repository/shacl_shapes/safety-shapes.ttl"]
        self.validation_error = False
    
    def set_coppola_config(self):
        tm_config = TMConfiguration()
        self.url_list = [self.coppola_endpoint + '/api/process?format=turtle',
                         self.coppola_endpoint + '/api/facility?format=turtle',
                         self.coppola_endpoint + '/api/resource?format=turtle',
                         self.coppola_endpoint + '/api/quality?format=turtle',
                         self.coppola_endpoint + '/api/safety?format=turtle']
    
    
    def validate(self):
        self.insert_shacl_shapes()

        payload = self.ttl
        headers = {
            'Content-Type': 'text/plain'
        }
        self.response_list = []
        for url in self.url_list:
            try:
                print("Sending ttl to validate it with process ontology")
                response = requests.request("POST", url, headers=headers, data=payload)
                print("Validation of " + url.split("/")[-1].split("?")[0] + " ontology was SUCCESSFULLY made")
                self.response_list.append(url.split("/")[-1].split("?")[0] + " : " + response.text)
            except:
                print("Error validating")
                self.validation_error = True
        print(self.response_list)

    def insert_shacl_shapes(self):
        for path in self.shacl_shapes_path:
            file = open(path, "r+")
            shacl = ' '.join(file.readlines())
            payload = shacl
            headers = {
                'Content-Type': 'text/plain'
            }
            try:
                shacl_id = path.split('/')[-1].replace("-shapes.ttl", "")
                print("Register Shacl Shape", shacl_id)
                response = requests.request("PUT", self.coppola_endpoint + "/api/" + shacl_id, headers=headers, data=payload)
                print("Shacl Shape " + shacl_id + " registered")
            except:
                print("Error registering Shacl Shape")
                self.handle_error()
                pass
            file.close()
    