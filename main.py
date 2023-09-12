#!/usr/bin/python3
from models import base_model, user
from datetime import datetime
from utils import hash_password

base = base_model.BaseModel()
user1 = user.User()
# format for datetime
time_format = "%Y-%m-%dT%H:%M:%S.%f"

dict = {
    "first_name": "Olamide",
    "last_name": "Bello",
    "email": "cloobtech@gmail.com",
    "password": "123456"
}

user2 = user.User(**dict)

print(user2.to_dict())
print(hash_password(dict['password']))
