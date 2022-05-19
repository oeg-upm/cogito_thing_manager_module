import json
import re
from wheezy.template.engine import Engine
from wheezy.template.ext.core import CoreExtension
from wheezy.template.loader import FileLoader

class TD_Service:
    def __init__(self, model):
        self.td_model = model
        self.template = None


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
        template_rendered = re.sub(r"[\n\t\s]*", "", template_rendered).replace(",}", "}").replace(",]", "]") # preprocess string before rendering to json format
        td = json.dumps(json.loads(template_rendered), indent=4) # rendered in json format and inedented
        print(td)

    def set_variables_to_render(self, prefixes, types, description, properties, actions, events, links):
        """
        Set variables to render the template
        """
        self.td_model.set_prefixes(prefixes)
        self.td_model.set_types(types)
        self.td_model.set_description(description)
        self.td_model.set_properties(properties)
        self.td_model.set_actions(actions)
        self.td_model.set_events(events)
        self.td_model.set_links(links)

    def info_to_render(self): # type element has to be added when the transformation is made
        """
        Retrieve info in a json format to render the template
        """
        self.td_model.set_info_to_render()

    
