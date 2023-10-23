#!/usr/bin/python3
import models
from models.user import User
from models.user_profile import UserProfile
from models.contribution import Contribution
from models.loan import Loan
from models.loan_refund import LoanRefund
from models.loan_profile import LoanProfile
from models.interest import Interest


user_dict1 = {
    'email': 'cloobtechse@gmail.com',
    'password': '123456',
    'reset_token': None
}

user_dict2 = {
    'email': 'belkid98@gmail.com',
    'password': '123456',
    'reset_token': None
}


d_contri1 = {
    'amount': 20000,
}
d_contri2 = {
    'amount': 10000,
}

# # Create their Profiles
user_pro1 = {
    'first_name': "Olamide",
    'last_name': 'Bello',
    'slot': 2,
    'registered': True,
    'month_covered': 0,
    'role': "admin"
}

user_pro2 = {
    'first_name': "Cloob",
    'last_name': 'Bello',
    'registered': True,
    'month_covered': 0,
    'role': "admin"
}
# Create User
user1 = User(**user_dict1)
user_profile1 = UserProfile(**user_pro1, user=user1)
user2 = User(**user_dict2)
user_profile2 = UserProfile(**user_pro2, user=user2)


# Create Contribution
contribution1 = Contribution(**d_contri1)
user_profile1.contributions.append(contribution1)
contribution2 = Contribution(**d_contri2)
user_profile2.contributions.append(contribution2)

# user_profile1.contribution.append(contribution1)
# user_profile1.contribution.append(contribution2)

models.storage.new(user1)
models.storage.new(user2)
models.storage.new(user_profile1)
models.storage.new(user_profile2)
models.storage.save()


x = models.storage.get_by_email('belkid98@gmail.com')
print(x)

# x = models.storage.get(UserProfile, 'bf1a1c5d-ba1f-4cfe-9620-bca429eb43f2')
# print(x.contributions[0].to_dict())
# x = models.storage.get(UserProfile, 'fa2a936c-37f9-4e59-beef-96c71c6c3f9b')
