from flask import Flask, json, send_file, request, make_response, jsonify, after_this_request

app = Flask(__name__)

@app.route("/project/<id>", methods=['GET'])
def get_project(id):
    """
    Retrieves the thing description of an existing project	
    """
    return "Get project with id: " + id

@app.route("/project/<id>", methods=['POST'])
def create_project(id):
    """
    Creates a new project, its respective triples and thing description
    """
    return "Created project with id: " + id

@app.route("/project/<id>", methods=['PUT'])
def update_project(id):
    """
    Updates an existing project, its respective triples and thing description
    """
    return "Updated project with id: " + id

@app.route("/project/<id>", methods=['DELETE'])
def delete_project(id):
    """
    Deletes an existing project, its respective triples and thing description, and also the thing descriptions associated to it in cascade mode
    """
    return "Delete project with id: " + id

@app.route("/project/<id>/file", methods=['POST'])
def add_file_to_project(id):
    """
    Adds a file/files to an existing project, creates respective triples and thing descriptions
    """
    return "Add file to project with id: " + id

@app.route("/project/<id>/file", methods=['DELETE'])
def delete_file_from_project(id):
    """
    Deletes file from project and its respective triples and thing descriptions
    """
    return "Delete file from project with id: " + id

@app.route("/project/<id>/file/ttl", methods=['POST'])
def process_ttl_file(id):
    """
    Retrieves from KGG the respective ttl file generated, saves it into the triple store and also generate respective thing descriptions for specific elements of the graph
    """
    return "TTL file retrieved with id: " + id



if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=8080)