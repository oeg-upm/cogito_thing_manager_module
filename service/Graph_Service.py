from rdflib import Graph
import hashlib
import uuid

class Graph_Service:
    def __init__(self, rdf):
        self.rdf = rdf
        self.graph = None
        self.file_id = None
        self.file_url = None
        self.query_files = """
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            PREFIX facility: <https://cogito.iot.linkeddata.es/def/facility#>
            PREFIX project: <https://cogito.iot.linkeddata.es/resources/project/>
            PREFIX platform: <https://cogito.iot.linkeddata.es/def/platform#>

            SELECT ?file WHERE {
                ?project platform:hasFile ?file .
            }
            """

        self.query_elements = """
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            PREFIX facility: <https://cogito.iot.linkeddata.es/def/facility#>

            SELECT ?element WHERE {
                ?element rdf:type facility:Element .
            }
        """

        self.query_remove_files = """
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            PREFIX facility: <https://cogito.iot.linkeddata.es/def/facility#>
            PREFIX project: <https://cogito.iot.linkeddata.es/resources/project/>
            PREFIX platform: <https://cogito.iot.linkeddata.es/def/platform#>

            DELETE { ?project platform:hasFile ?file } WHERE {
                ?project platform:hasFile ?file .
            }
        """
        
    def parse_graph(self):
        self.graph = Graph()
        self.graph.parse(data=self.rdf, format="turtle")
        

    def query_graph(self, query):
        results = self.graph.query(query)
        return results
    

    def update_graph(self, query):
        self.graph.update(query)


    def get_files(self):
        results = self.query_graph(self.query_files)
        if len(results) != 0:
            for row in results:
                hash_value = hashlib.sha256(str(row.file).encode('utf-8'))
                self.file_id = hash_value.hexdigest()
                self.file_url = str(row.file)

    def define_random_uuid(self):
        self.file_id = str(uuid.uuid4())