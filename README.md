# cogito_thing_manager_module
Thing Manager module for the COGITO project.

- [ ] Thing Manager communication table
	- [ ] POST /project/{:id}
		- [x] Definition
		- [x] Process
		- [ ] Handle Errors
	- [ ] PUT /project/{:id}
		- [x] Definition
		- [ ] Process
		- [ ] Handle Errors
	- [ ] DELETE /project/{:id}
		- [x] Definition
		- [ ] Process
		- [ ] Handle Errors
	- [ ] GET /project/{:id}
		- [x] Definition
		- [ ] Process
		- [ ] Handle Errors
	- [ ] POST /project/{:id}/{:format_of_file}/{:name_of_file} --> they can add more than one file inside the json sent
		- [x] Definition
		- [ ] Process
		- [ ] Handle Errors
	- [ ] DELETE /project/{:id}/{:format_of_file}/{:name_of_file}
		- [x] Definition
		- [ ] Process
		- [ ] Handle Errors
	- [ ] POST {:id}/{:format_of_file}/{:name_of_file}/ttl
		- [x] Definition
		- [ ] Process
		- [ ] Handle Errors

| Method | Headers                           | Endpoints               | Description                                                                                                                                                             | Parameters                                                                                                    |
| ------ | --------------------------------- | ----------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------- |
| POST   | Content-Type: application/json    | /project/{:id}          | Creates a new project, its respective triples and thing description                                                                                                     | id(mandatory), name(optional), description(optional)                                                          |
| PUT    | Content-Type: application/json    | /project/{:id}          | Updates an existing project, its respective triples and thing description                                                                                               | id(mandatory), name(optional), description(optional)                                                          |
| DELETE | N/A                               | /project/{:id}          | Deletes an existing project, its respective triples and thing description, and also the thing descriptions associated to it in cascade mode                             | id(mandatory)                                                                                                 |
| GET    | N/A                               | /project/{:id}          | Retrieves the thing description of an existing project                                                                                                                  | id(mandatory)                                                                                                 |
| POST   | Content-Type: application/json    | /project/{:id}/file     | Adds a file/files to an existing project, creates respective triples and thing descriptions                                                                             | id(mandatory), format_of_file(mandatory), type_of_file(mandatory), uri_of_file(mandatory), metadata(optional) |
| DELETE | N/A                               | /project/{:id}/file     | Deletes file from project and its respective triples and thing descriptions                                                                                             | id(mandatory), format_of_file(mandatory), type_of_file(mandatory), uri_of_file(mandatory), metadata(optional) |
| POST   | Content-Type: multipart-form/data | /project/{:id}/file/ttl | Retrieves from KGG the respective ttl file generated, saves it into the triple store and also generate respective thing descriptions for specific elements of the graph | id(mandatory), format_of_file(mandatory), type_of_file(mandatory), name_of_file(mandatory)                    |

- [ ] Communication with KGG modules via SSE (Server Sends Events)
- [ ] Handle configuration with config.json file


# For Server Sent Events Install

- [ ] REDIS
  - [ ] execution --> redis-server
  - [ ] https://hub.docker.com/_/redis/

- [ ] Channels
  - [ ] /stream --> SSE
  - [ ] /stream?channel=x
    - [ ] error --> channel=error
    - [ ] project --> channel=project
    - [ ] schedule --> channel=file.schedule --> establecer pre-procesados
    - [ ] ifc --> channel=file.ifc
    - [ ] file --> channel=file --> para extras
    - [ ] visual_qc --> channel=file.visual_qc