

class Errors:
    def __init__(self):
        self.__error_number = None
        self.__error_description = None


    def get_error_number(self):
        return self.__error_number

    def get_error_description(self):
        return self.__error_description
    
    def set_error_number(self, error_number):
        self.__error_number = error_number

    def set_error_description(self, error_description):
        self.__error_description = error_description
        
    def to_json(self):
        return {
            "error_number": self.get_error_number(),
            "error_description": self.get_error_description()
        }