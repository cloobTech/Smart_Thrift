#!/usr/bin/python3
from models import base_model
from datetime import datetime

base = base_model.BaseModel()
base3 = base_model.Base()
# format for datetime
time_format = "%Y-%m-%dT%H:%M:%S.%f"

dict = {
    "id": "123",
    "created_at": "2021-06-28T16:30:40.100000",
    "updated_at": "2021-06-28T16:30:00.000000",
    "name": "Holberton"
}

base2 = base_model.BaseModel(**dict)

print(base.to_dict())