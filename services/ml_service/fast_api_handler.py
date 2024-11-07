import pickle
import pandas as pd
import logging

MODEL_PATH = "./models/model.pkl"

class FastApiHandler:

    def __init__(self):

        self.param_types = {
            "user_id": str,
            "model_params": dict
        }

        self.model_path = MODEL_PATH
        self.load_model(model_path=self.model_path)

        self.required_model_params = [
            'id',
            'floor',
            'is_apartment',
            'kitchen_area',
            'living_area',
            'rooms',
            'studio',
            'total_area',
            'build_year',
            'building_type_int',
            'latitude',
            'longitude',
            'ceiling_height',
            'flats_count',
            'floors_total',
            'has_elevator'
        ]
    

    def load_model(self, model_path: str):
        """Функция для загрузки модели

        Args:
            model_path (str): путь до модели
        """
        try:
            with open(model_path, "rb") as model_file:
                self.model = pickle.load(model_file)
                
        except FileNotFoundError:
            print(f'Model file not found: {model_path}')
            raise
        except pickle.UnpicklingError:
            print('Failed to load model due to unpickling error')
            raise


    def predict(self, model_params: dict) -> int:
        """Функция для получения предсказания модели

        Args:
            model_params (dict): параметры для модели

        Returns:
            int: Предсказание стоимости квартиры
        """
        
        param_values_list = pd.DataFrame([model_params])

        try:
            prediction = int(self.model.predict(param_values_list)[0])
        except ValueError as e:
            print(f'Value error during prediction: {e}')
            raise
        except Exception as e:
            print(f'Failed to make prediction: {e}')
            raise
        
        return prediction
    

    def check_required_query_params(self, query_params: dict) -> bool:
        """Проверяем параметры запроса на наличие обязательного набора.
        
        Args:
            query_params (dict): Параметры запроса.
        
        Returns:
            bool: True — если есть нужные параметры, False — иначе
        """       

        if "model_params" not in query_params or "user_id" not in query_params:
            return False
        
        if not isinstance(query_params["model_params"], self.param_types["model_params"]):
            return False
        
        if not isinstance(query_params["user_id"], self.param_types["user_id"]):
            return False
        
        return True
    

    def check_required_model_params(self, model_params: dict) -> bool:
        """Проверяем параметры для получения предсказаний.

        Args:
            model_params (dict): Параметры пользователя для предсказания.

        Returns:
            bool: True — если есть нужные параметры, False — иначе
        """
        if set(model_params.keys()) == set(self.required_model_params):
            return True
        return False
    
    def validate_params(self, params: dict) -> bool:
        """Проверяем корректность параметров запроса и параметров модели.

        Args:
            params (dict): Словарь параметров запроса.

        Returns:
            bool: True — если пройдены проверки, False — иначе
        """

        if self.check_required_query_params(params):
            print("All query params exist")
        else:
            print("Not all query params exist")
            return False

        if self.check_required_model_params(params["model_params"]):
            print("All model params exist")
        else:
            print("Not all model params exist")
            return False
        
        return True

    
    def handle(self, params):
        """Функция для обработки входящих запросов по API. Запрос состоит из параметров.

        Args:
            params (dict): Словарь параметров запроса.

        Returns:
            dict: Словарь, содержащий результат выполнения запроса.
        """

        if not self.validate_params(params):
            logging.error("Validation failed for parameters: %s", params)
            return {"Error": "Problem with parameters"}

        user_id = params["user_id"]
        model_params = params["model_params"]
        
        try:
            prediction = self.predict(model_params)
            return {
                "user_id": user_id,
                "prediction": prediction
            }
        
        except ValueError as e:
            logging.error("Value error during prediction: %s", e)
            return {"Error": "Invalid values in model parameters"}
        
        except FileNotFoundError as e:
            logging.error("Model file not found: %s", e)
            return {"Error": "Model file not found"}
        
        except Exception as e:
            logging.exception("Unexpected error while handling request: %s", e)
            return {"Error": "Problem with request"}
        

if __name__ == "__main__":

    test_params = {
        "user_id": '123',
        "model_params": {
            "id": 50968,
            "floor": 3,
            "is_apartment": False,
            "kitchen_area": 9.7,
            "living_area": 18.9,
            "rooms": 1,
            "studio": False,
            "total_area": 35.0,
            "build_year": 1988,
            "building_type_int": 4,
            "latitude": 55.886028,
            "longitude": 37.658363,
            "ceiling_height": 2.48,
            "flats_count": 474,
            "floors_total": 16,
            "has_elevator": True
        }
    }


    handler = FastApiHandler()

    response = handler.handle(test_params)
    print(f"Response: {response}")