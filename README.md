# cogito_thing_manager_module
Thing Manager module for the COGITO project.

- [ ] Thing Manager communication table
	- [x] POST /project/{:id}
		- [x] Definition
		- [x] Process
		- [x] Handle Errors
	- [x] PUT /project/{:id}
		- [x] Definition
		- [x] Process
		- [x] Handle Errors
	- [x] DELETE /project/{:id}
		- [x] Definition
		- [x] Process
		- [x] Handle Errors
	- [x] POST /project/{:id}/{:format_of_file}/{:name_of_file} --> they can add more than one file inside the json sent
		- [x] Definition
		- [x] Process
		- [x] Handle Errors
	- [ ] DELETE /project/{:id}/{:format_of_file}/{:name_of_file}
		- [x] Definition
		- [ ] Process
		- [x] Handle Errors
	- [x] POST {:id}/{:format_of_file}/{:name_of_file}/ttl
		- [x] Definition
		- [x] Process
		- [x] Handle Errors

| Method | Headers                           | Endpoints               | Description                                                                                                                                                             | Parameters                                                                                                    |
| ------ | --------------------------------- | ----------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------- |
| POST   | Content-Type: application/json    | /project/{:id}          | Creates a new project, its respective triples and thing description                                                                                                     | id(mandatory), name(optional), description(optional)                                                          |
| PUT    | Content-Type: application/json    | /project/{:id}          | Updates an existing project, its respective triples and thing description                                                                                               | id(mandatory), name(optional), description(optional)                                                          |
| DELETE | N/A                               | /project/{:id}          | Deletes an existing project, its respective triples and thing description, and also the thing descriptions associated to it in cascade mode                             | id(mandatory)                                                                                                 |
| GET    | N/A                               | /project/{:id}          | Retrieves the thing description of an existing project                                                                                                                  | id(mandatory)                                                                                                 |
| POST   | Content-Type: application/json    | /project/{:id}/file     | Adds a file/files to an existing project, creates respective triples and thing descriptions                                                                             | id(mandatory), format_of_file(mandatory), type_of_file(mandatory), uri_of_file(mandatory), metadata(optional) |
| DELETE | N/A                               | /project/{:id}/file     | Deletes file from project and its respective triples and thing descriptions                                                                                             | id(mandatory), format_of_file(mandatory), type_of_file(mandatory), uri_of_file(mandatory), metadata(optional) |
| POST   | Content-Type: multipart-form/data | /project/{:id}/file/ttl | Retrieves from KGG the respective ttl file generated, saves it into the triple store and also generate respective thing descriptions for specific elements of the graph | id(mandatory), format_of_file(mandatory), type_of_file(mandatory), name_of_file(mandatory)                    |

- [x] Communication with KGG modules via SSE (Server Sends Events)
- [x] Handle configuration with config.json file


# For Server Sent Events Install

- [x] REDIS
  - [x] execution --> redis-server
  - [x] https://hub.docker.com/_/redis/

- [x] Channels
  - [x] /stream --> SSE
  - [x] /stream?channel=x
    - [x] project --> channel=project
    - [x] schedule --> channel=file.schedule --> establecer pre-procesados
    - [x] ifc --> channel=file.ifc
    - [x] file --> channel=file --> para extras
    - [x] visual_qc --> channel=file.visual_qc