import json
import re
from wheezy.template.engine import Engine
from wheezy.template.ext.core import CoreExtension
from wheezy.template.loader import FileLoader

class TD:
    def __init__(self, id, file_id = None):
        self.__id = {"id" : id} # None
        self.__file_id = file_id # None
        self.__prefixes = {"prefixes" : []} # List of dicts
        self.__types = {"types" : []} # List
        self.__title = {"title" : None} # None
        self.__description = {"description" : None} # None
        self.__properties = {"properties" : []} # List of dicts
        self.__actions = {"actions" : []} # List of dicts
        self.__events = {"events" : []} # List of dicts
        self.__links = {"links" : []} # List of dicts
        self.__security = {"security" : None} # List of dicts
        self.__template_path = "./templates/"
        self.__template_name = "td.template.edge"
        self.__render_info = {}
    
    def set_info_to_render(self): # concatenate all info to info_to_render with predefined variables
        """
        Set info to render the template
        """
        self.__render_info = {
            **self.get_id(),
            **self.get_title(),
            **self.get_prefixes(),
            **self.get_types(),
            **self.get_description(),
            **self.get_properties(),
            **self.get_actions(),
            **self.get_events(),
            **self.get_links()
        }

    def get_info_to_render(self):
        """
        Get info to render the template
        """
        return self.__render_info
    
    def set_title(self, title):
        """
        Set title of the TD
        """
        self.__title["title"] = title

    def get_title(self):
        """
        Get title of the TD
        """
        return self.__title

    def set_properties(self, properties):
        """
        Set properties of the TD
        """
        self.__properties["properties"] = properties

    def get_properties(self):
        """
        Get properties of the TD
        """
        return self.__properties

    def set_actions(self, actions):
        """
        Set actions of the TD
        """
        self.__actions["actions"] = actions

    def get_actions(self):
        """
        Get actions of the TD
        """
        return self.__actions

    def set_events(self, events):
        """
        Set events of the TD
        """
        self.__events["events"] = events

    def get_events(self):
        """
        Get events of the TD
        """
        return self.__events

    def set_links(self, links):
        """
        Set links of the TD
        """
        self.__links["links"] = links

    def get_links(self):
        """
        Get links of the TD
        """
        return self.__links
        

    def set_security(self, security):
        """
        Set security of the TD
        """
        self.__security["security"] = security

    def get_security(self):
        """
        Get security of the TD
        """
        return self.__security

    def set_prefixes(self, prefixes):
        """
        Set prefixes of the TD
        """
        self.__prefixes["prefixes"] = prefixes

    def get_prefixes(self):
        """
        Get prefixes of the TD
        """
        return self.__prefixes

    def set_types(self, types):
        """
        Set types of the TD
        """
        self.__types["types"] = types

    def get_types(self):
        """
        Get types of the TD
        """
        return self.__types

    def set_description(self, description):
        """
        Set description of the TD
        """
        self.__description["description"] = description

    def get_description(self):
        """
        Get description of the TD
        """
        return self.__description

    def set_id(self, id):
        """
        Set id of the TD
        """
        self.__id = {"id" : id}

    def get_id(self):
        """
        Get id of the TD
        """
        return self.__id

    def get_file_id(self):
        """
        Get file id of the TD
        """
        return self.__file_id

    def get_template_path(self): # +1
        """
        Get template path
        """
        return self.__template_path

    def get_template_name(self): # +1
        """
        Get template name
        """
        return self.__template_name