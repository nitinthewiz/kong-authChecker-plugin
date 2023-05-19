# README

## About
This is a Kong plugin to check authentication for a user. It assumes that the user sends a request to the Kong API gateway endpoint with a header that is used for authentication. The name of the header item is variable (default is 'token'). The value, however, must be a base64 encoded string of the format - "<email>:<password>". 

This string is decoded to be passed to a remote server which authenticates the user. If the request is authentic, the remote server returns a 200 OK as well as a JWT 'accessToken' along with other identifying information about the user in a JSON body. This accessToken is then added to the upstream request as a header item. The name of this header item is also configurable (default is 'token').


## Manual playground
#### Prep
1. Assuming the system has a relatively new version of node and Python 3.x
2. Install python requirements 
    1. either directly to the system using `pip install -r requirements.txt` or 
    2. install a virtual environment using `python3 -m venv /temp/kong-py-pdk` and activate it using `source /temp/kong-py-pdk/bin/activate` and then install using pip as above
3. Run `setup_instruction.sh`


#### Schema
auth_server_url                        - 
auth_server_response_body_field_name   - 
request_header_field_name              - 
upstream_request_header_field_name     - 
ttl                                    - 

## Instructions

### Testing
#### Prep
1. Assuming the system has a relatively new version of node and Python 3.x
2. Install python requirements 
    1. either directly to the system using `pip install -r requirements.txt` or 
    2. install a virtual environment using `python3 -m venv /temp/kong-py-pdk` and activate it using `source /temp/kong-py-pdk/bin/activate` and then install using pip as above
3. 

#### Unit
`python3 -m unittest tests/unit.py `

`python3 -m coverage run -m unittest tests/unit.py`

`python3 -m coverage report`

#### Integration -