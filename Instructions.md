# Инструкции по запуску микросервиса

Каждая инструкция выполняется из директории репозитория mle-sprint3-completed
Если необходимо перейти в поддиректорию, напишите соотвесвтующую команду

## 1. FastAPI микросервис в виртуальном окружение
```bash
# команды создания виртуального окружения
# и установки необходимых библиотек в него
python3 -m venv .venv
source .venv/bin/activate
pip install -r services/requirements.txt

# команда перехода в директорию
cd services

# команда запуска сервиса с помощью uvicorn
uvicorn ml_service.app:app --reload --port 8081 --host 0.0.0.0
```

### Пример curl-запроса к микросервису

```bash
curl -X 'POST' \
  'http://127.0.0.1:8081/api/churn/?user_id=123' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "id": 50968,
  "floor": 3,
  "is_apartment": false,
  "kitchen_area": 9.7,
  "living_area": 18.9,
  "rooms": 1,
  "studio": false,
  "total_area": 35,
  "build_year": 1988,
  "building_type_int": 4,
  "latitude": 55.886028,
  "longitude": 37.658363,
  "ceiling_height": 2.48,
  "flats_count": 474,
  "floors_total": 16,
  "has_elevator": true
}'
```


## 2. FastAPI микросервис в Docker-контейнере

```bash
# команда перехода в нужную директорию
cd services

# команда для запуска микросервиса в режиме docker container
docker image build -f Dockerfile_ml_service . --tag ml_service:1
docker container run -d --publish 8081:8081 --volume=./models:/ml_service/models --env-file .env ml_service:1
```

### Пример curl-запроса к микросервису

```bash
curl -X 'POST' \
  'http://127.0.0.1:8081/api/churn/?user_id=123' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "id": 50968,
  "floor": 3,
  "is_apartment": false,
  "kitchen_area": 9.7,
  "living_area": 18.9,
  "rooms": 1,
  "studio": false,
  "total_area": 35,
  "build_year": 1988,
  "building_type_int": 4,
  "latitude": 55.886028,
  "longitude": 37.658363,
  "ceiling_height": 2.48,
  "flats_count": 474,
  "floors_total": 16,
  "has_elevator": true
}'
```

## 3. Docker compose для микросервиса и системы мониторинга

```bash
# команда перехода в нужную директорию
cd services

# команда для запуска микросервиса в режиме docker compose
docker compose up --build -d
```
После запуска нужно перенаправить порты 9090 и 3000

### Пример curl-запроса к микросервису

```bash
curl -X 'POST' \
  'http://localhost:8081/api/churn/?user_id=123' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "id": 50968,
  "floor": 3,
  "is_apartment": false,
  "kitchen_area": 9.7,
  "living_area": 18.9,
  "rooms": 1,
  "studio": false,
  "total_area": 35,
  "build_year": 1988,
  "building_type_int": 4,
  "latitude": 55.886028,
  "longitude": 37.658363,
  "ceiling_height": 2.48,
  "flats_count": 474,
  "floors_total": 16,
  "has_elevator": true
}'
```

###

## 4. Скрипт симуляции нагрузки
Скрипт генерирует 50 запросов в течение 120 секунд

```bash
cd requests_simulation
python simulate.py
```

Адреса сервисов:
- микросервис: http://localhost:8081
- Prometheus: http://localhost:9090
- Grafana: http://localhost:3000