# README

## About
**Warning** - This plugin is not meant to be used in production. This is a POC. There are more feature complete authentication plugins available within Kong.

This is a Kong plugin to check authentication for a user. It assumes that the user sends a request to the preconfigured Kong API gateway endpoint with a header that is used for authentication. The name of the header item is variable (default is 'token'). The value, however, must be a base64 encoded string of the format - "<email>:<password>". 

This header value is decoded to be passed to a remote authentication server which authenticates the user. If the request is authentic, the remote server returns a 200 OK as well as a JWT access token along with other identifying information about the user in a JSON body. This access token is then added to the upstream request as a header item. The name of the upstream header item is also configurable (default is 'token').

For all cases where the authentication server does not respond with a 200 OK, the plugin makes Kong return HTTP Status code 401 (Unauthorized) with the error message "Invalid authentication credentials". This is part of the reason why this plugin should not be used in production yet. The error handling can and should be more detailed, specifically around cases like the authentication server being unavailable, and the user not providing the request header.

#### Schema
| Name | Usage | Default |
| ------------- | ------------- |                                                                           
| auth_server_url | This is the URL of the authentication server. The server should take an email and password as a payload and return a JWT. Tested with json-server and json-server-auth. | http://host.docker.internal:3000/login |
| auth_server_response_body_field_name | This is the field in the body of the authentication server's successful response that would then be passed on to the upstream server as a JWT. | accessToken |
| request_header_field_name | This is the header name that the user must include in their initial request to Kong. The format should be base64 encoded "email:password" | token |
| upstream_request_header_field_name | This is the header name that will be included by the authChecker plugin in the upstream request, after succesful authentication from the authentication server. | token |

## Manual playground
#### Prep
1. Assuming the system has a relatively new version of node and Python 3.x
2. Install python requirements 
    1. either directly to the system using `pip install -r requirements.txt` or 
    2. install a virtual environment using `python3 -m venv /temp/kong-py-pdk` and activate it using `source /temp/kong-py-pdk/bin/activate` and then install using pip as above
3. Run `setup_instruction.sh` to create the network, build the docker image from the Dockerfile, create and setup the postgres database to be used by Kong, as well as setup `json-server-auth` with the included db.json file. The db is initialized with the email mail@nitinkhanna.com and the password `bestPassw0rd`. You may replace the same by hitting the /register endpoint. Instructions for the same are [here](https://www.npmjs.com/package/json-server-auth).
4. Run `start-kong.sh` to start Kong API Gateway. Note that we run kong-gateway because we like the webUI.
5. Also note that we run Kong with the preconfigured kong.yml file. This allows for a faster setup. You can modify the file as required. Leave it empty if you want to configure Kong from scratch.
6. Also note that the webUI is on port 8002 as standard in Kong but the public endpoint is on 8003 instead of 8000. This is because the developer uses portainer, which runs on port 8000.
7. Once you're done testing Kong, run the `stop-kong.sh` script to only stop Kong, or directly run the `cleanup_instructions.sh` file to remove all artifacts - Kong gateway, postgres container, docker network, as well as to stop the `json-server-auth`

### Testing
#### Prep
1. Assuming the system has a relatively new version of node and Python 3.x
2. Install python requirements 
    1. either directly to the system using `pip install -r requirements.txt` or 
    2. install a virtual environment using `python3 -m venv /temp/kong-py-pdk` and activate it using `source /temp/kong-py-pdk/bin/activate` and then install using pip as above
3. Once inside, you can run the unit testing using the commands given below. Note that the integration test only requires docker as the setup and execution of tests happens inside the purpose-built docker container.

#### Unit
To run the unit tests and generate code coverage information for the authChecker plugin - 
`python -m coverage run --include plugins/authChecker.py -m unittest tests/unit.py`

To display the coverage report as well as fail if under 80% coverage, which is the industry standard -
`python -m coverage report --fail-under 80`

#### Integration -
To run the integration test, simply run the following command - 
`bash tests/integration.sh`

### TODO
1. Improve HTTP status codes
2. Test with more authentication backends
3. Add TTL for JWT. Currently DAOs are not supported by the Kong python PDK. So the plugin can use `sqlite-cache` for the purpose. `json-server-auth` responds with an JWT that expires in 1 hour.