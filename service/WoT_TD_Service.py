from configparser import NoOptionError
from hashlib import new
import json
import re
from time import sleep
from turtle import title
from xml.dom import NoModificationAllowedErr
from wheezy.template.engine import Engine
from wheezy.template.ext.core import CoreExtension
from wheezy.template.loader import FileLoader
import ast
from rdflib import Graph

class TD_Service:
    def __init__(self, model, flag, project_identifier=None, file_identifier=None):
        self.project_identifier = project_identifier
        self.file_identifier = file_identifier
        self.td_model = model
        self.template = None
        self.thing_description = None
        self.query_results = None
        self.graph = None
        self.json_template = None
        self.properties = []
        self.actions = []
        self.events = []
        self.links = []
        self.metadata = {}
        self.flag = flag

    def load_template(self):
        """
        Loads the template to create TDs
        """
        searchpath = [self.td_model.get_template_path()] # search path
        engine = Engine(
            loader=FileLoader(searchpath),
            extensions=[CoreExtension()]
        ) # generate engine
        self.template = engine.get_template(self.td_model.get_template_name()) # load template

    
    def generate_td(self):
        """
        Generate Thing Descriptions by rendering templates
        """
        template_rendered = self.template.render(self.td_model.get_info_to_render()) # rendered in str format
        template_rendered = re.sub(r"[\n\t]*", "", template_rendered).replace(",}", "}").replace(",]", "]") # preprocess string before rendering to json format
        self.thing_description = ast.literal_eval(template_rendered)

    def set_variables_to_render(self):
        """
        Set variables to render the template
        """
        if self.flag:
            self.td_model.set_id(self.metadata["id"])
        self.td_model.set_title(self.metadata["title"])
        self.td_model.set_prefixes(self.metadata["prefixes"])
        self.td_model.set_types(self.metadata["type"])
        self.td_model.set_description(self.metadata["description"])
        self.td_model.set_properties(self.properties)
        self.td_model.set_actions(self.actions)
        self.td_model.set_events(self.events)
        self.td_model.set_links(self.links)

    def info_to_render(self): # type element has to be added when the transformation is made
        """
        Retrieve info in a json format to render the template
        """
        self.td_model.set_info_to_render()
        return self.td_model.get_info_to_render()

    
    def load_json_template(self, json_template_path):
        """
        Loads the json template to create TDs
        """
        # Dependiendo del tipo de TD se carga el json template
        with open(json_template_path, 'r') as json_file:
            self.json_template = json.load(json_file)
            json_file.close()

    def load_graph(self, graph_data):
        """
        Loads the graph to create TDs
        """
        self.graph = Graph()
        self.graph.parse(data=graph_data, format="turtle")

    def execute_sparql_query(self):
        """
        Executes a sparql query
        """
        self.query_results = self.graph.query(self.json_template["sparql"])


    def def_properties(self):
        """
        Defines the properties to be used in the template
        """
        for property in self.json_template["thing_description"]["properties"]:
            print("property", property)
            if " !! multiple !! " in property["href"]:
                multiple_dict = self.exchange_values(property, multiple=True, external = False)
                self.properties.append(multiple_dict)
            elif " !! external_id !! " in property["href"] or " !! external_file_id !! " in property["href"]:
                external_value = self.exchange_values(property, multiple=False, external=True, identifier=self.project_identifier, file_identifier=self.file_identifier)
                print("external_value", external_value)
                self.properties.append(external_value)
            else:
                new_value = self.exchange_values(property, multiple=False, external = False)
                self.properties.append(new_value)

    def def_actions(self):
        """
        Defines the actions to be used in the template
        """
        for action in self.json_template["thing_description"]["actions"]:
            if " !! multiple !! " in action["href"]:
                multiple_dict = self.exchange_values(action, True)
                self.actions.append(multiple_dict)
            elif " !! external_id !! " in action["href"] or " !! external_file_id !! " in action["href"]:
                external_value = self.exchange_values(action, multiple=False, external=True, identifier=self.project_identifier, file_identifier=self.file_identifier)
                self.actions.append(external_value)
            else:
                new_value = self.exchange_values(action, False)
                self.actions.append(new_value)

    def def_events(self):
        """
        Defines the events to be used in the template
        """
        for event in self.json_template["thing_description"]["events"]:
            if " !! multiple !! " in event["href"]:
                multiple_dict = self.exchange_values(event, True)
                self.events.append(multiple_dict)
            elif " !! external_id !! " in event["href"] or " !! external_file_id !! " in event["href"]:
                external_value = self.exchange_values(event, multiple=False, external=True, identifier=self.project_identifier, file_identifier=self.file_identifier)
                self.events.append(external_value)
            else:
                new_value = self.exchange_values(event, False)
                self.events.append(new_value)

    def def_links(self):
        """
        Defines the links to be used in the template
        """
        for link in self.json_template["thing_description"]["links"]:
            if " !! multiple !! " in link["href"]:
                multiple_dict = self.exchange_values(link, True)
                for elem in multiple_dict["multiple_"+link["rel"]]:
                    self.links.append(elem)
            elif " !! external_id !! " in link["href"] or " !! external_file_id !! " in link["href"]:
                external_value = self.exchange_values(link, multiple=False, external=True, identifier=self.project_identifier, file_identifier=self.file_identifier)
                self.links.append(external_value)
            else:
                new_value = self.exchange_values(link, False)
                self.links.append(new_value)

    def def_metadata(self):
        """
        Defines the metadata to be used in the template
        """
        for metadata in self.json_template["thing_description"]:
            if metadata != "properties" and metadata != "actions" and metadata != "events" and metadata != "links":
                if self.flag and metadata == "id":
                    if " ?? " in self.json_template["thing_description"][metadata]:
                        new_value = self.exchange_values(self.json_template["thing_description"][metadata], False)
                        self.metadata.update({"id" : new_value})
                if metadata == "title":
                    if " ?? " in self.json_template["thing_description"][metadata]:
                        new_value = self.exchange_values(self.json_template["thing_description"][metadata], False)
                        self.metadata.update({"title" : new_value})
                    else:
                        new_value = self.json_template["thing_description"][metadata]
                        self.metadata.update({"title" : new_value})
                if metadata == "type":
                    if " ?? " in self.json_template["thing_description"][metadata]:
                        new_value = self.exchange_values(self.json_template["thing_description"][metadata], False)
                        self.metadata.update({"type" :  new_value})
                    else:
                        new_value = self.json_template["thing_description"][metadata]
                        self.metadata.update({"type" : new_value})
                if metadata == "description":
                    if " ?? " in self.json_template["thing_description"][metadata]:
                        new_value = self.exchange_values(self.json_template["thing_description"][metadata], False)
                        self.metadata.update({"description" : new_value})
                    else:
                        new_value = self.json_template["thing_description"][metadata]
                        self.metadata.update({"description" : new_value})
                if metadata == "prefixes":
                    self.metadata.update({"prefixes" : self.json_template["thing_description"][metadata]})


    def exchange_values(self, for_value, multiple=None, external=None, identifier=None, file_identifier=None):
        """
        Exchange the values of the of the template with the query results values
        """
        if multiple:
            key = ""
            if "name" in for_value:
                key = "name"
                multiple_dict = {"multiple_"+for_value[key] : []}
            elif "rel" in for_value:
                key = "rel"
                multiple_dict = {"multiple_"+for_value[key] : []}
            for row in self.query_results:
                new_value = for_value.copy()
                for label in row.labels:
                    string_label = " !! multiple !! ?? " + label + " ?? "
                    if string_label in for_value["href"]:
                        new_value["href"] = new_value["href"].replace(string_label, row[label])
                        multiple_dict["multiple_"+for_value[key]].append(new_value)
            return multiple_dict
        elif external and identifier != "None" and file_identifier != "None":
            if isinstance(for_value, dict):
                new_value = for_value.copy()
                string_label_id = " !! external_id !! "
                string_label_file_id = " !! external_file_id !! "
                if string_label_id in for_value["href"]:
                    new_value["href"] = new_value["href"].replace(string_label_id, identifier)
                if string_label_file_id in for_value["href"]:
                    new_value["href"] = new_value["href"].replace(string_label_file_id, file_identifier)
                return new_value
        else:
            if isinstance(for_value, dict):
                for row in self.query_results:
                    #sleep(1)
                    #print("hello, query results",[row[0] for row in self.query_results]) # DO NOT REMOVE
                    new_value = for_value.copy()
                    for label in row.labels:
                        string_label = " ?? " + label + " ?? "
                        if string_label in for_value["href"]:
                            new_value["href"] = new_value["href"].replace(string_label, row[label])
                            return new_value
            elif isinstance(for_value, str):
                for row in self.query_results:
                    new_value = for_value
                    for label in row.labels:
                        string_label = " ?? " + label + " ?? "
                        if string_label in for_value:
                            new_value = new_value.replace(string_label, row[label])
                            return new_value
            