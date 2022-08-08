import requests
import json

class WoT_Hive_Controller():
    def __init__(self, wot_hive_url):
        self.wot_hive_url = wot_hive_url
        self.predetermined_td = None



    def get_td(self, id): # get thing description with provided id
        url = self.wot_hive_url + "api/things/" + id
        payload={}
        headers = {
        'Content-Type': 'application/td+json'
        }
        response = requests.request("GET", url, headers=headers, data=payload)
        return response



    def post_td(self, id, td):
        url = self.wot_hive_url + "api/things/" + id
        payload = json.dumps(td)
        headers = {
        'Content-Type': 'application/td+json'
        }
        response = requests.request("PUT", url, headers=headers, data=payload)



    def update_td(self, id, data): # update project thing descriptions
        response = self.get_td(id)
        td = json.loads(response.text)
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

    def predetermined_td_set(self, id):
        self.predetermined_td = {
            "@context": [
                "https://www.w3.org/2019/wot/td/v1",
                {
                    "facility": "https://cogito.iot.linkeddata.es/def/facility#"
                },
                "https://w3c.github.io/wot-discovery/context/discovery-context.jsonld"
            ],
            "id": id,
            "securityDefinitions": {
                "nosec_sc": {
                    "scheme": "nosec"
                }
            },
            "description": "Project description",
            "links": [],
            "properties": {
                "ValueInGraph": {
                    "forms": [
                        {
                            "href": "http://data.cogito.iot.linkeddata.es/resources/Project_"+id,
                            "type": "text/turtle"
                        }
                    ]
                },
                "KnowledgeGraph": {
                    "forms": [
                        {
                            "href": "https://data.cogito.linkeddata.es/resources/"+id,
                            "type": "text/turtle"
                        }
                    ]
                }
            },
            "title": "Project "+id,
            "types": "https://cogito.iot.linkeddata.es/def/facility#Project",
            "security": [
                "nosec_sc"
            ]
        }