from fastapi import FastAPI, Body
from .fast_api_handler import FastApiHandler
from prometheus_fastapi_instrumentator import Instrumentator
from prometheus_client import Histogram, Counter

app = FastAPI()
app.handler = FastApiHandler()

instrumentator = Instrumentator()
instrumentator.instrument(app).expose(app)

ml_service_predictions = Histogram(
    "ml_service_predictions",
    "Histogram of predictions",
    buckets = (1e6, 2e6, 5e6, 1e7, 2.5e7)
)


ml_service_prediction_counter = Counter(
    "ml_service_prediction_counter",
    "Counter of predcitions"
)



@app.get("/")
def read_root():
    return "Сервис предсказания цены на квартиру"

@app.post("/api/churn/")
def get_prediction_for_item(
    user_id: str,
    model_params: dict = Body(
        example={
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
    )
) -> dict:
    """Функция для получения предсказания стоимости квартиры.

    Args:
        model_params (dict): Параметры квартиры, которые мы должны подать в модель.

    Returns:
        dict: Предсказание стоимости.
    """
    all_params = {
        "user_id": user_id,
        "model_params": model_params
    }

    response = app.handler.handle(params=all_params)

    prediction = response["prediction"]

    ml_service_predictions.observe(prediction)
    ml_service_prediction_counter.inc()

    return response