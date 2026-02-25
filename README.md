# 🔍 Dirty Data Detective: Sensor Data Validation with Pydantic

**Проект по очистке и валидации "грязных" данных от сенсоров с использованием Pydantic для строгого контроля входящих данных.**

## 📋 О проекте

Это **обучающий проект** для инженеров данных и разработчиков, которые хотят научиться:
- Работать с неконсистентными данными из внешних источников
- Использовать Pydantic для строгой валидации схемы данных
- Правильно обрабатывать ошибки валидации
- Применять best practices для очистки данных в AI/ML пайплайнах

### Суть задачи

Представь, что сенсоры отправляют данные, но качество хромает:
- ❌ Некоторые значения — не того типа (строка вместо float)
- ❌ Отсутствуют обязательные поля
- ❌ Появляются лишние неописанные поля
- ❌ Встречаются None и NaN

Задача — **приручить этот хаос** с помощью Pydantic и Pandas!

---

## 📂 Структура проекта

```
Dirty-Data/
├── sensor_validation.py    # Основной скрипт с валидацией
├── messy_data.json         # "Грязные" данные для тестирования
├── venv/                   # Виртуальное окружение Python
└── README.md               # Этот файл
```

---

## 🛠️ Технический стек

- **Python 3.x** — язык разработки
- **Pydantic v2** — валидация и парсинг данных с использованием ConfigDict
- **Pandas** — работа с табличными данными (DataFrame)
- **JSON** — формат хранения тестовых данных
- **Git & GitHub** — версионирование и коллаборация

---

## 🚀 Быстрый старт

### 1. Клонируй репозиторий

```bash
git clone https://github.com/vsanyanov-ux/Dirty-Data.git
cd Dirty-Data
```

### 2. Создай и активируй venv

**На Windows (PowerShell):**
```powershell
python -m venv venv
venv\Scripts\Activate.ps1
```

**На macOS / Linux:**
```bash
python -m venv venv
source venv/bin/activate
```

### 3. Установи зависимости

```bash
pip install pandas pydantic
```

### 4. Запусти скрипт

```bash
python sensor_validation.py
```

---

## 📊 Как это работает

### Шаг 1: Грязные данные

```json
[
  {"sensor_id": "A1", "temperature_c": 25.5, "humidity_percent": 60, "location": "Room1", "extra_field": "oops"},
  {"sensor_id": "B2", "temperature_c": "30", "humidity_percent": 55},
  {"sensor_id": "C3", "temperature_c": 22, "location": "Room2"},
  {"sensor_id": "D4", "temperature_c": 18.0, "humidity_percent": 70, "timestamp": "2023-10-26T10:00:00Z"},
  {"sensor_id": "E5", "temperature_c": null, "humidity_percent": 65, "location": "Room3"}
]
```

**Проблемы:** лишние поля, пропуски, неверные типы данных, None-значения.

### Шаг 2: Pydantic-модель со строгой валидацией

```python
from pydantic import BaseModel, ConfigDict
from typing import Optional

class SensorReading(BaseModel):
    model_config = ConfigDict(extra='forbid')  # Запрет любых неописанных полей!
    
    sensor_id: str
    temperature_c: float  # Обязательное поле
    humidity_percent: int  # Обязательное поле
    location: Optional[str] = None  # Опциональное поле
```

**Ключевой момент:** `extra='forbid'` — это **первая линия обороны** против грязных данных!

### Шаг 3: Загрузка в DataFrame и валидация

```python
import pandas as pd
from pydantic import ValidationError

df = pd.DataFrame(messy_records)
errors = []

for idx, row in df.iterrows():
    data = row.to_dict()
    data = {k: v for k, v in data.items() if pd.notna(v)}  # Убираем NaN
    try:
        reading = SensorReading(**data)
    except ValidationError as e:
        errors.append((idx, e))
```

### Шаг 4: Отчёт об ошибках

Скрипт выводит все ошибки валидации с указанием:
- 🔴 Номер строки в DataFrame
- 🔴 Тип ошибки (extra_forbidden, missing, type mismatch)
- 🔴 Описание проблемы

**Пример вывода:**
```
Ошибки валидации:

Row 0:
1 validation error for SensorReading
extra_field
  Extra inputs are not permitted [type=extra_forbidden, input_value='oops', input_type=str]

Row 2:
1 validation error for SensorReading
humidity_percent
  Field required [type=missing, ...]

Row 4:
1 validation error for SensorReading
temperature_c
  Field required [type=missing, ...]
```

---

## 💡 Ключевые концепции

### 1. Pydantic ConfigDict vs старый class Config

✅ **Современный подход (v2):**
```python
model_config = ConfigDict(extra='forbid')
```

❌ **Устаревший подход (будет удалён в v3):**
```python
class Config:
    extra = 'forbid'
```

### 2. Почему extra='forbid' критично?

Без этого параметра Pydantic молча игнорирует неизвестные поля — это может привести к:
- 🚨 Потере данных
- 🚨 Непредсказуемым ошибкам в системе
- 🚨 Проблемам отладки

**С extra='forbid':** всё неизвестное отклоняется сразу, на входе.

### 3. Виртуальные окружения (venv)

Каждый проект должен иметь изолированное окружение:
- Зависимости не смешиваются с глобальной системой
- Разные проекты могут использовать разные версии библиотек
- Легко поделиться требованиями через `requirements.txt`

---

## 📈 Уровни сложности задач

| Задача | Сложность | Что учится |
|--------|-----------|------------|
| Создание грязных данных | ⭐☆☆☆☆ | Структурирование данных, JSON |
| Pydantic-модель | ⭐⭐⭐☆☆ | ConfigDict, типизация, Pydantic v2 |
| Загрузка в Pandas | ⭐⭐☆☆☆ | DataFrame, работа с табличными данными |
| Валидация через Pydantic | ⭐⭐⭐⭐☆ | Обработка ошибок, ETL-подход, инженерные практики |
| Работа с venv | ⭐⭐☆☆☆ | Виртуальные окружения, pip, изоляция зависимостей |

---

## 🔧 Дальнейшее развитие

Сейчас скрипт только выявляет ошибки. Следующие шаги:

- [ ] Реализовать **автоматическую очистку данных**
  - Конвертировать строку `"30"` → `30.0`
  - Заполнять пропуски средним значением или дефолтом
  - Отбрасывать или лечить лишние поля
- [ ] Добавить **кастомные валидаторы**
  - Диапазоны для температуры и влажности
  - Проверка формата sensor_id
- [ ] Сохранять **чистые данные** в CSV/JSON
- [ ] Добавить **логирование** ошибок валидации
- [ ] Покрыть код **unit-тестами**

---

## 📚 Полезные ресурсы

- [Pydantic Official Docs](https://docs.pydantic.dev/)
- [Pydantic V2 Migration Guide](https://docs.pydantic.dev/2.0/migration/)
- [Pandas Documentation](https://pandas.pydata.org/docs/)
- [Python Virtual Environments](https://docs.python.org/3/tutorial/venv.html)

---

## 🎓 Чему ты научился на этом проекте

✅ Создавать Pydantic-модели со строгой валидацией  
✅ Запрещать неизвестные поля через `extra='forbid'`  
✅ Обрабатывать ValidationError без падения программы  
✅ Работать с DataFrame и итерироваться по строкам  
✅ Использовать виртуальные окружения (venv)  
✅ Публиковать код на GitHub  
✅ Писать документацию (README)  

---

## 👨‍💻 Автор

**Ваня** (vsanyanov-ux) — Junior Data Engineer, обучается лучшим практикам работы с данными.

---

## 📄 Лицензия

Мит лицензия (MIT) — используй как хочешь!

---

**Удачи, детектив грязных данных! 🔍✨**
