"""
Kong authentication check plugin
"""

# !/usr/bin/env python3
import base64
import kong_pdk.pdk.kong as kong
import requests

Schema = (
    {"auth_server_url": {"type": "string"}},
    {"auth_server_response_body_field_name": {"type": "string"}},
    {"request_header_field_name": {"type": "string"}},
    {"upstream_request_header_field_name": {"type": "string"}},
    {"ttl": {"type": "number"}},
)

VERSION = '0.1.0'
PRIORITY = 0


class Plugin(object):
    """Default plugin class to start the plugin. Contains the access phase 
    where this plugin operates."""
    def __init__(self, config):
        self.config = config

    def access(self, kong: kong.kong):
        """This plugin primarily works in the access phase.
           - It uses the request_header_field_name to find the authentication
           information from the incoming request. It is assumed that the
           authentication header value is base64 encoded "email:password".
           - Then it calls the auth_server_url with the extracted login
           information.
           - If it receives a 200 OK response from the auth server, the
           plugin sets the upstream_request_header_field_name to the JWT
           recieved before passing on the request to the upstream server.
           - If at any point any of the steps fail, the plugin sends back
           a HTTP 401 status with "Invalid authentication credentials" message.
        """
        request_header_field_value = "user:pass"

        request_header_field_name = "token"
        if 'request_header_field_name' in self.config:
            request_header_field_name = self.config['request_header_field_name']

        try:
            request_header_field_value = kong.request.get_header(
                request_header_field_name)
            if request_header_field_value is None:
                raise TypeError
        except Exception:
            return kong.response.exit(401, "Invalid authentication credentials")

        auth_server_url = "http://host.docker.internal:3000/login"
        if 'auth_server_url' in self.config:
            auth_server_url = self.config['auth_server_url']

        payload_values = base64.b64decode(request_header_field_value).decode()
        payload_values_split = payload_values.split(":")

        payload = {
            "email": payload_values_split[0],
            "password": payload_values_split[1]
        }
        headers = {"Content-Type": "application/json"}

        response = requests.request("POST", auth_server_url,
                                    json=payload, headers=headers)

        try:
            if response is None:
                raise TypeError
        except Exception:
            return kong.response.exit(401, "Invalid authentication credentials")

        if response.status_code == 200:
            upstream_request_header_field_name = "token"
            if 'upstream_request_header_field_name' in self.config:
                upstream_request_header_field_name = self.config['upstream_request_header_field_name']

            auth_server_response_body_field_name = "accessToken"
            if 'auth_server_response_body_field_name' in self.config:
                auth_server_response_body_field_name = self.config['auth_server_response_body_field_name']
            kong.service.request.set_header(upstream_request_header_field_name,
                                            response.json()[auth_server_response_body_field_name])
        else:
            return kong.response.exit(401, "Invalid authentication credentials")


if __name__ == "__main__":
    """Add this section to allow this plugin optionally be running in a
    dedicated process
    """
    from kong_pdk.cli import start_dedicated_server
    start_dedicated_server("authChecker", Plugin, VERSION, PRIORITY, Schema)
