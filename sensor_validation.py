import json

with open("messy_data.json", "w") as f:
    json.dump(messy_records, f, ensure_ascii=False, indent=2)

from pydantic import BaseModel, ConfigDict, field_validator
from typing import Optional

class SensorReading(BaseModel):
    model_config = ConfigDict(extra='forbid')

    sensor_id: str
    temperature_c: float
    humidity_percent: int
    location: Optional[str] = None # новый стиль конфигурации Pydantic v2

    @field_validator("temperature_c", mode="before")
    def parse_temperature(cls, v):
        if v is None:
            return v
        # допускаем строки вида "23.5", " 23,5 " и т.п.
        if isinstance(v, str):
            v = v.strip().replace(",", ".")
            if v == "":
                return None
        return float(v)


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

