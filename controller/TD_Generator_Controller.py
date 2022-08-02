from model.WoT_TD_model import TD
from service.WoT_TD_Service import TD_Service

import json

class TD_Generator_Controller:
    

    def __init__(self, id, type_of_td, hierarchy_level, graph_data, hierarchy_parent=None, file_id=None):
        self.file_id = file_id
        self.graph_data = graph_data
        self.json_template_path = None
        self.json_template_path_child = None
        self.td = None
        self.child_td_list = []
        self.td_type = type_of_td
        self.hierarchy_level = hierarchy_level
        self.thing_descriptions = []
       
        if hierarchy_level == 0:
            self.model = TD(id) # Here goes the id of the project
            self.service = TD_Service(self.model, False)
        elif hierarchy_level == 1:
            self.model = TD(self.file_id) # Here goes the id of the file
            self.hierarchy_parent = hierarchy_parent
            self.service = TD_Service(self.model, False, project_identifier=id, file_identifier=self.file_id)
        else:
            self.model = TD("no_identifier")
            # for every id element in graph, create new thing description
            self.hierarchy_parent = hierarchy_parent
            self.service = TD_Service(self.model, True, project_identifier=id, file_identifier=self.file_id)

    def pick_json_templates_by_type(self):
        """
        Picks the json template by type
        """
        if self.td_type == "project":
            self.json_template_path = "json_templates/project.json"
        elif self.td_type == "ifc":
            self.json_template_path = "json_templates/ifc.json"
        elif self.td_type == "ifc_elements":
            self.json_template_path = "json_templates/ifc_elements.json"
        elif self.td_type == "schedule":
            self.json_template_path = "json_templates/schedule.json"
            #self.json_template_path_child = "json_templates/schedule_elements.json"
        elif self.td_type == "resource_types":
            self.json_template_path = "json_templates/resource_types.json"
            #self.json_template_path_child = "json_templates/resource_types_elements.json"
        else:
            pass
    
    def load_controller(self, json_template_path):
        """
        Loads the templates to create TDs
        """
        self.service.load_json_template(json_template_path)
        self.service.load_graph(self.graph_data)

    def generate_td(self):
        """
        Generate Thing Descriptions by rendering templates
        """
        self.service.load_template()
        self.service.set_variables_to_render()
        info_to_render = self.service.info_to_render()
        self.service.generate_td()
        self.td = self.service.thing_description

    def execute_sparql_query(self):
        """
        Executes a sparql query
        """
        self.service.execute_sparql_query()

    def provide_values_to_render(self):
        """
        Provides values to render the template
        """
        self.service.def_properties()
        self.service.def_actions()
        self.service.def_events()
        self.service.def_links()
        self.service.def_metadata()

    def main(self):
        """
        Main function
        """
        self.pick_json_templates_by_type()
        self.load_controller(self.json_template_path)
        self.execute_sparql_query()
        if self.hierarchy_level != 2:
            self.provide_values_to_render()
            self.generate_td()
        else:
            # extract values from sparql query
            # for every id element in graph, create new thing description
            query_results = self.service.query_results
            for result in query_results:
                self.service.query_results = [result]
                self.provide_values_to_render()
                self.generate_td()
                self.thing_descriptions.append(self.td)