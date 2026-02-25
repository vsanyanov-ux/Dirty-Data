import json

messy_records = [
    {"sensor_id": "A1", "temperature_c": 25.5, "humidity_percent": 60, "location": "Room1", "extra_field": "oops"},
    {"sensor_id": "B2", "temperature_c": "30", "humidity_percent": 55},
    {"sensor_id": "C3", "temperature_c": 22, "location": "Room2"},
    {"sensor_id": "D4", "temperature_c": 18.0, "humidity_percent": 70, "timestamp": "2023-10-26T10:00:00Z"},
    {"sensor_id": "E5", "temperature_c": None, "humidity_percent": 65, "location": "Room3"}
]

with open("messy_data.json", "w") as f:
    json.dump(messy_records, f, ensure_ascii=False, indent=2)

from pydantic import BaseModel, ConfigDict
from typing import Optional

class SensorReading(BaseModel):
    model_config = ConfigDict(extra='forbid')

    sensor_id: str
    temperature_c: float
    humidity_percent: int
    location: Optional[str] = None # новый стиль конфигурации Pydantic v2


import pandas as pd

with open("messy_data.json", "r") as f:
    messy_records = json.load(f)

df = pd.DataFrame(messy_records)
print(df)

from pydantic import ValidationError

errors = []
valid_readings = []

for idx, row in df.iterrows():
    data = row.to_dict()
    # Уберём NaN, чтобы не превращались в лишние поля
    data = {k: v for k, v in data.items() if pd.notna(v)}
    try:
        reading = SensorReading(**data)
        valid_readings.append((idx, reading))
    except ValidationError as e:
        errors.append((idx, e))

print("Ошибки валидации:")
for idx, err in errors:
    print(f"\nRow {idx}:")
    print(err)

# --- новый маленький шаг: сохраняем результат в файлы ---

# Валидные записи -> чистый датасет
valid_df = pd.DataFrame([r.model_dump() for _, r in valid_readings])
valid_df.to_csv("clean_sensor_data.csv", index=False)

# Ошибки -> отдельный отчёт
error_rows = []
for idx, err in errors:
    error_rows.append({
        "row_index": idx,
        "errors": str(err).replace("\n", " | ")
    })

errors_df = pd.DataFrame(error_rows)
errors_df.to_csv("sensor_data_errors.csv", index=False)

print("Сохранено clean_sensor_data.csv и sensor_data_errors.csv")

