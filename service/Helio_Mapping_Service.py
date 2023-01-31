from wheezy.template.engine import Engine
from wheezy.template.ext.core import CoreExtension
from wheezy.template.loader import FileLoader

class Helio_Mapping_Service:
    def __init__(self):
        self.template = None
        self.mapping_template_name = None
        
    def load_template(self):
        """
        Load the template
        """
        searchpath = ["./templates/"] # search path
        engine = Engine(
            loader=FileLoader(searchpath),
            extensions=[CoreExtension()]
        ) # generate engine
        self.template = engine.get_template(self.mapping_template_name) # load template

    def generate_mapping(self, info_to_render, mapping_template_name):
        """
        Generate the mapping
        """
        self.mapping_template_name = mapping_template_name
        self.load_template()
        return self.template.render(info_to_render)