import requests
import time
import json

def convert_value(key, value):
    type_mapping = {
        'id': int,
        'floor': int,
        'rooms': int,
        'build_year': int,
        'building_type_int': int,
        'flats_count': int,
        'floors_total': int,
        'is_apartment': lambda x: x.lower() == 'true',
        'studio': lambda x: x.lower() == 'true',
        'has_elevator': lambda x: x.lower() == 'true',
        'kitchen_area': float,
        'living_area': float,
        'total_area': float,
        'price': float,
        'ceiling_height': float,
        'latitude': float,
        'longitude': float,
    }
    
    if key in type_mapping:
        converter = type_mapping[key]
        return converter(value) if not callable(converter) else converter(value)
    
    return value

with open('simulate.csv', 'r') as file:
    model_param_keys = [x for x in file.readline().strip().split(',')]
    for i, line in enumerate(file.readlines()):
        model_param_values = line.strip().split(',')

        model_params = {
            model_param_keys[j]: convert_value(model_param_keys[j], model_param_values[j]) for j in range(len(model_param_keys))
        }

        print(model_params)
        response = requests.post(f'http://localhost:8081/api/churn/?user_id={i}', json=model_params)

        if response.status_code != 200:
            print(f"Error {response.status_code}: {response.text}")

        if i == 30:
            time.sleep(20)
        time.sleep(2)