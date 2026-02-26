import json
from pydantic import BaseModel, ConfigDict, field_validator
from typing import Optional

class SensorReading(BaseModel):
    model_config = ConfigDict(extra='forbid')

    sensor_id: str
    temperature_c: float
    humidity_percent: int
    location: Optional[str] = None # новый стиль конфигурации Pydantic v2

    # --- Исправляем некорректные данные в температуре --
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

# Топ типов ошибок
error_stats = (
    errors_df["errors"]
    .value_counts()
    .reset_index()
    .rename(columns={"index": "error_type", "errors": "count"})
)

error_stats.to_csv("sensor_error_stats.csv", index=False)

print("\nТоп ошибок:")
print(error_stats)


# data quality summary по датасету 
total_rows = len(df)
valid_rows = len(valid_df)
error_rows_count = len(errors_df)

valid_share = valid_rows / total_rows * 100 if total_rows else 0
error_share = error_rows_count / total_rows * 100 if total_rows else 0

print(f"Всего строк: {total_rows}")
print(f"Валидных: {valid_rows} ({valid_share:.1f}%)")
print(f"С ошибками: {error_rows_count} ({error_share:.1f}%)")


