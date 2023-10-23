#!/usr/bin/python3
import models
from models.user import User
from models.user_profile import UserProfile

email = 'email'
email2 = 'belkid98@gmail.com'


# X = UserProfile.__mapper__.relationships.user.argument()
user_model = UserProfile.user.property.mapper.class_
y = getattr(user_model, email)

print(user_model)
print(type(user_model))
print(y)
