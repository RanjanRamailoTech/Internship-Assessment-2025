# utils.py
import json
from pathlib import Path

def merge_swagger_json(server1_path, server2_path, output_path):
    """Merge two Swagger JSON files from local paths and save to a file."""
    try:
        # Read Server 1 JSON
        print("file1")
        with open(server1_path, 'r') as f1:
            server1_swagger = json.load(f1)
        print(f"Loaded Server 1 JSON from {server1_path}")

        # Read Server 2 JSON
        with open(server2_path, 'r') as f2:
            print("file2")
            
            server2_swagger = json.load(f2)
        print(f"Loaded Server 2 JSON from {server2_path}")

        # Merge "info" sections
        merged_info = {
            "title": "Combined API Documentation",
            "version": "1.0",
            "description": "Combined Swagger documentation for Server 1 (Stocks) and Server 2 (Users)"
        }

        # Merge "paths" sections
        merged_paths = server1_swagger['paths'].copy()
        merged_paths.update(server2_swagger['paths'])

        # Merge "components" sections
        merged_components = server1_swagger.get('components', {}).copy()
        server2_components = server2_swagger.get('components', {})
        for key, value in server2_components.items():
            if key in merged_components:
                merged_components[key].update(value)
            else:
                merged_components[key] = value

        # Merge "tags" sections
        merged_tags = server1_swagger.get('tags', []).copy()
        merged_tags.extend(server2_swagger.get('tags', []))

        # Create merged Swagger JSON
        merged_swagger = {
            "openapi": "3.0.0",
            "info": merged_info,
            "paths": merged_paths,
            "components": merged_components,
            "tags": merged_tags
        }

        # Save to file
        with open(output_path, 'w') as f:
            json.dump(merged_swagger, f, indent=2)
        print(f"Merged Swagger JSON saved to {output_path}")

    except FileNotFoundError as e:
        print(f"Error: File not found - {e}")
    except json.JSONDecodeError as e:
        print(f"JSON decode error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

if __name__ == "__main__":
    # Replace these with your actual file paths
    SERVER1_JSON_PATH = 'server1.json'
    SERVER2_JSON_PATH = 'server2.json'
    OUTPUT_PATH = Path(__file__).resolve().parent / 'combined_swagger.json'
    
    merge_swagger_json(SERVER1_JSON_PATH, SERVER2_JSON_PATH, OUTPUT_PATH)