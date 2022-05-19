from rdflib import Graph
from SPARQLWrapper import SPARQLWrapper, JSON

class TripleStore_Controller:
    def __init__(self, data, project_id, file_id = None):
        self.graph = None
        self.data = data
        self.sparql_endpoint_select = SPARQLWrapper("http://localhost:7200/repositories/cogito-triplestore")
        self.sparql_endpoint = SPARQLWrapper("http://localhost:7200/repositories/cogito-triplestore/statements")
        self.project_id = project_id
        self.file_id = file_id
        self.select_results = None

    def serialize_graph(self):
        self.graph = Graph()
        self.graph.parse(data=self.data, format="turtle")
        self.graph = self.graph.serialize(format="nt")

    def create_graph(self):
        self.serialize_graph()
        self.sparql_endpoint.method = "POST"
        self.sparql_endpoint.setHTTPAuth("DIGEST")
        self.sparql_endpoint.setCredentials("admin", "admin")
        if self.file_id != None:
            self.get_named_graphs()
            for result in self.select_results["results"]["bindings"]:
                if "https://data.cogito.iot.linkeddata.es/" + self.project_id in result['g']['value']:
                    self.sparql_endpoint.setQuery("INSERT DATA { GRAPH <https://data.cogito.iot.linkeddata.es/"+self.project_id + "/" + self.file_id + "> { " + self.graph + " } }")
                    self.sparql_endpoint.query()
                    self.sparql_endpoint.setQuery("INSERT DATA { GRAPH <https://data.cogito.iot.linkeddata.es/"+self.project_id + "> { " + self.graph + " } }")
                    self.sparql_endpoint.query()
        else:
            self.sparql_endpoint.setQuery("INSERT DATA { GRAPH <https://data.cogito.iot.linkeddata.es/"+self.project_id + "> { " + self.graph + " } }")
            self.sparql_endpoint.query()
        

    def delete_graph(self):
        self.sparql_endpoint.method = "POST"
        self.sparql_endpoint.setHTTPAuth("DIGEST")
        self.sparql_endpoint.setCredentials("admin", "admin")
        if self.file_id != None:
            self.sparql_endpoint.setQuery("CLEAR GRAPH <https://data.cogito.iot.linkeddata.es/" + self.project_id + "/" + self.file_id + ">")
            self.sparql_endpoint.query()
        else:
            self.get_named_graphs()
            for result in self.select_results["results"]["bindings"]:
                if "https://data.cogito.iot.linkeddata.es/" + self.project_id in result['g']['value']:
                    self.sparql_endpoint.setQuery("CLEAR GRAPH <" + result['g']['value'] + ">")
                    self.sparql_endpoint.query()
        

    def get_named_graphs(self):
        self.sparql_endpoint_select.method = "GET"
        self.sparql_endpoint_select.setReturnFormat(JSON)
        self.sparql_endpoint_select.setHTTPAuth("DIGEST")
        self.sparql_endpoint_select.setCredentials("admin", "admin")
        self.sparql_endpoint_select.setQuery("SELECT DISTINCT ?g WHERE { GRAPH ?g { ?s ?p ?o } }")
        self.select_results = self.sparql_endpoint_select.queryAndConvert()