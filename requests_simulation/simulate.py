import requests
import time
import json

def convert_value(key, value):
    if key in ['id', 'floor', 'rooms', 'build_year', 'building_type_int', 'flats_count', 'floors_total']:
        return int(value)
    elif key in ['is_apartment', 'studio', 'has_elevator']:
        return value.lower() == 'true'
    elif key in ['kitchen_area', 'living_area', 'total_area', 'price', 'ceiling_height', 'latitude', 'longitude']:
        return float(value)
    else:
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