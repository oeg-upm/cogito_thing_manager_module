from service.Helio_Mapping_Service import Helio_Mapping_Service
import requests

class Helio_Mapping_Controller:
    def __init__(self, project_id, file_id, rdf, helio_endpoint):
        self.mapping_service = Helio_Mapping_Service()
        self.info_to_render_sigle = {
            "rdf" : rdf,
            "project_id" : project_id,
            "file_id" : file_id,
            "ontologies_shapes" : "https://raw.githubusercontent.com/oeg-upm/cogito_data_repository/main/shapes/all_shapes.ttl"
        }
        self.info_to_render_consistency = {
            "project_id" : project_id,
            "consistency_shape" : "https://raw.githubusercontent.com/oeg-upm/cogito_data_repository/main/demo_example_SHACL/shape.ttl",
        }
        self.helio_endpoint = helio_endpoint
        self.mapping = None
        self.data = None

    def post_mapping(self, mapping_id): # mapping_id = "single_mapping"
        """
        Post the mapping
        """
        url = self.helio_endpoint + "/api/" + mapping_id
        payload = self.mapping
        headers = {
            'Content-Type': 'text/plain'
        }
        print("Update Helio Mapping")
        response = requests.request("POST", url, headers=headers, data=payload)

    def get_mapping_data(self, mapping_id): # mapping_id = "/api/single_mapping"
        """
        Get the mapping result
        """
        url = self.helio_endpoint + "/api/" + mapping_id + "/data"

        payload={}
        headers = {}

        print("Retrieving Helio Mapping Data")
        response = requests.request("GET", url, headers=headers, data=payload)
        print("Helio Mapping Data Retrieved")
        self.data = response.text.replace("\n\n\n", "").replace("\n\n", "")

    def generate_single_mapping(self, mapping_template_name):
        """
        Generate the relevant mapping
        """
        self.mapping = self.mapping_service.generate_mapping(self.info_to_render_sigle, mapping_template_name)
        

    def generate_consistency_mapping(self, mapping_template_name):
        """
        Generate the consistency mapping
        """
        self.mapping = self.mapping_service.generate_mapping(self.info_to_render_consistency, mapping_template_name)

    def modify_project_id(self, project_id):
        """
        Modify the project id
        """
        self.info_to_render_consistency = {
            "project_id" : project_id,
            "consistency_shape" : "https://raw.githubusercontent.com/oeg-upm/cogito_data_repository/main/demo_example_SHACL/shape.ttl",
        } 