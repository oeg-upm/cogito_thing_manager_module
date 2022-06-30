import requests
import json

class WoT_Hive_Controller():
    def __init__(self):
        self.wot_hive_url = "http://localhost:9000/"



    def get_td(self, id): # get thing description with provided id
        url = self.wot_hive_url + "api/things/" + id
        payload={}
        headers = {
        'Content-Type': 'application/td+json'
        }
        response = requests.request("GET", url, headers=headers, data=payload)
        return response.text



    def post_td(self, id, td):
        url = self.wot_hive_url + "api/things/" + id
        payload = json.dumps(td)
        headers = {
        'Content-Type': 'application/td+json'
        }
        response = requests.request("PUT", url, headers=headers, data=payload)



    def update_td(self, id, data): # update project thing descriptions
        td = json.loads(self.get_td(id))
        if "links" in td:
            td["links"].append(data)
        else:
            td["links"] = [data]
        self.post_td(id, td)



    def delete_td(self, id):
        url = self.wot_hive_url + "api/things/" + id
        payload={}
        headers = {
        'Content-Type': 'application/td+json'
        }
        response = requests.request("DELETE", url, headers=headers, data=payload)
        return response.text