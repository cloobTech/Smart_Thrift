#!/usr/bin/python3
import models
from models.user import User
from models.user_profile import UserProfile

email = 'email'
email2 = 'belkid98@gmail.com'

X = models.storage.get_by_attribute(User, email, email2)

print(X)