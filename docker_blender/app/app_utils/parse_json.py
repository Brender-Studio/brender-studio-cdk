import json

def parse_json(json_str):
    try:
        json_data = json.loads(json_str)
        # print(json.dumps(json_data, indent=2)) 
        return json_data
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
        return None