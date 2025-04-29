import json
import requests

import yaml
import requests


# URLs of the Swagger JSON files (replace with actual URLs)
server1_swagger_url = 'http://localhost:8002/swagger.json'  # Replace with actual URL
server2_swagger_url = 'http://localhost:8001/swagger.json'  # Replace with actual URL

# Function to fetch Swagger YAML from a URL and convert it to a dictionary
def fetch_swagger_yaml(url):
    response = requests.get(url)
    if response.status_code == 200:
        return yaml.safe_load(response.text)  # Convert YAML to Python dict
    else:
        print(f"Error fetching {url}: {response.status_code}")
        return None

# Fetch Swagger YAML files from both servers
server1_swagger = fetch_swagger_yaml(server1_swagger_url)
server2_swagger = fetch_swagger_yaml(server2_swagger_url)

# Ensure that both Swagger YAMLs are fetched successfully
if server1_swagger and server2_swagger:
    # Merge the info sections (you can customize this further if needed)
    merged_info = {
        "title": "Combined API Documentation",
        "description": "Combined Swagger documentation for Server 1 and Server 2",
        "version": "1.0"
    }

    # Merge the paths sections
    merged_paths = server1_swagger['paths'].copy()
    merged_paths.update(server2_swagger['paths'])  # Add Server 2 paths to Server 1 paths

    # Merge the definitions sections (schemas, responses, etc.)
    merged_definitions = server1_swagger.get('definitions', {}).copy()
    server2_definitions = server2_swagger.get('definitions', {})
    merged_definitions.update(server2_definitions)

    # Merge the securityDefinitions sections
    merged_security_definitions = server1_swagger.get('securityDefinitions', {}).copy()
    server2_security_definitions = server2_swagger.get('securityDefinitions', {})
    merged_security_definitions.update(server2_security_definitions)

    # Create the final merged Swagger YAML (you can convert it back to YAML later if needed)
    merged_swagger = {
        "swagger": "2.0",
        "info": merged_info,
        "host": "localhost:8000",  # Modify the host if needed
        "schemes": ["http"],
        "basePath": "/api",
        "consumes": ["application/json"],
        "produces": ["application/json"],
        "paths": merged_paths,
        "definitions": merged_definitions,
        "securityDefinitions": merged_security_definitions,
        "security": [{"Basic": []}],
    }

    # Save the merged Swagger YAML to a file
    with open('merged_swagger.yaml', 'w') as f:
        yaml.dump(merged_swagger, f, default_flow_style=False)

    print("Merged Swagger YAML has been saved as 'merged_swagger.yaml'")

else:
    print("Error: One or both Swagger YAML files could not be fetched.")
