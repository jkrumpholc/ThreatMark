import datetime
import requests
import fastapi
from typing import Literal
import json
import os

boxes = {}
app = fastapi.FastAPI()


class Cache:
    filename: str

    def __init__(self, timestamp: datetime.datetime):
        self.filename = timestamp.strftime("%Y_%m_%d_%H_%M_%S")

    def read(self) -> dict:
        if self.filename is not None:
            with open(self.filename, 'r', encoding='utf-8') as f:
                return json.loads(f.read())

    def write(self, content: str) -> None:
        with open(self.filename, 'w', encoding='utf-8') as f:
            f.write(content)

    def delete(self) -> None:
        if os.path.exists(self.filename):
            os.remove(self.filename)


class Config:
    name: str
    unit: str
    value: str
    timestamp: datetime.datetime

    def __init__(self, unit: str, timestamp: str, value: str):
        match unit:
            case '%':
                self.name = "Humidity"
            case '°C':
                value = (float(value) * 1.8) + 32
                unit = '°F'
                self.name = "Temperature"
            case '°F':
                self.name = "Temperature"
            case _:
                self.name = "None"
        self.unit = unit
        self.timestamp = datetime.datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%S.%fZ')
        self.value = value

    def __str__(self):
        return f"{self.name}: {self.value}{self.unit} Measured on: {self.timestamp.strftime('%A, %d. %B %Y %I:%M%p')}"


class Data:
    configs: list[Config]

    def __init__(self, data: dict):
        self.configs = []
        self.parse_data(data)

    def parse_data(self, data: dict) -> None:
        for sensor in data['sensors']:
            match sensor['unit']:
                case '%' | '°C' | '°F':
                    self.configs.append(
                        Config(
                            sensor['unit'],
                            sensor['lastMeasurement']['createdAt'],
                            sensor['lastMeasurement']['value']
                        )
                    )
                case _:
                    continue

    def __str__(self):
        return "\n".join([sensor.__str__() for sensor in self.configs])



class Box:
    box_id: str
    file_format: Literal["json", "geojson"] = "json"
    last_read: datetime.datetime
    cache: Cache | None
    data: list[Data]

    def __init__(self, box_id: str, file_format: Literal["json", "geojson"] = "json"):
        self.box_id = box_id
        self.last_read = datetime.datetime.min
        self.cache = None
        self.data = []
        self.sensors = []
        if file_format is not None:
            self.file_format = file_format

    def api_read(self):
        if datetime.datetime.now() - self.last_read > datetime.timedelta(minutes=5):
            request = requests.get(f'https://api.opensensemap.org/boxes/{self.box_id}?format={self.file_format}')
            if request.status_code == 200:
                self.last_read = datetime.datetime.now()
                try:
                    self.cache.delete()
                except AttributeError as e:
                    pass
                self.cache = Cache(self.last_read)
                self.cache.write(request.text)
                self.data.append(Data(request.json()))
                return False
        else:
            self.data.append(Data(self.cache.read()))
            return True


@app.get("/box/{box_id}")
async def get_box_data(box_id: str):
    if box_id not in boxes:
        box = Box(box_id=box_id)
        boxes[box_id] = box
        return {"Success": True, "Box": box.box_id}
    else:
        return {"Success": False, "Reason": "Box already exists"}


@app.get("/{box_id}/read_api")
async def get_read_api(box_id: str):
    if box_id not in boxes:
        return {"Success": False, "Reason": "Box does not exists"}
    from_cache = boxes[box_id].api_read()
    return {"Success": True, "Box": boxes[box_id].box_id, "Timestamp": boxes[box_id].last_read, "Read_from_cache": from_cache}


@app.get("/{box_id}/print_data")
async def print_box(box_id: str):
    if box_id not in boxes:
        return {"Success": False, "Reason": "Box does not exists"}
    print(data for data in boxes[box_id].data)
    return {
        "Success": True,
        "Box": boxes[box_id].box_id,
        "Data": (data.__str__() for data in boxes[box_id].data)
    }
