#!/usr/bin/python3
import models
from models.user import User
from models.user_profile import UserProfile
from models.contribution import Contribution

# from faker import Faker
from faker import Faker
import random

fake = Faker()

# Function to generate a random user dictionary


def generate_user():
    user_dict = {
        'email': fake.email(),
        'password': fake.password(),
        'reset_token': None
    }
    return user_dict

# Function to generate a random user profile dictionary


def generate_user_profile():
    user_profile = {
        'first_name': fake.first_name(),
        'last_name': fake.last_name(),
        'slot': random.randint(1, 4),
        'registered': fake.boolean(),
        'month_covered': random.randint(0, 2)
    }
    return user_profile


user_instances = []


# Contribution
def generate_contribution():
    contribution = {
        "amount": 10000
    }

    return contribution


# Generate 50 user dictionaries
users = [generate_user() for _ in range(50)]

# Generate 50 user profile dictionaries
user_profiles = [generate_user_profile() for _ in range(50)]

# Print the first user and user profile as an example
contribution = [generate_contribution() for _ in range(50)]

for user_dict, user_profile_dict, contribution in zip(users, user_profiles, contribution):
    # Create User instance
    user = User(**user_dict)
    contribution = Contribution(**contribution)

    # Create UserProfile instance with a reference to the User instance
    user_profile = UserProfile(**user_profile_dict, user=user)
    user_profile.contributions.append(contribution)
    models.storage.new(user_profile)

    # Add the user and user profile instances to the list
    user_instances.append((user, user_profile))

models.storage.save()
