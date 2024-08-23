from faker import Faker
import numpy as np
import pandas as pd
import random
import string

fake = Faker()

def generate_user_id():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))

# Generate user data
users = pd.DataFrame({
    'User ID': [generate_user_id() for _ in range(500)],
    'Name': [fake.name() for _ in range(500)],
    'Date of Birth': [fake.date_of_birth(minimum_age=18, maximum_age=90) for _ in range(500)],
    'Gender': [fake.random_element(elements=('Male', 'Female')) for _ in range(500)],
    'Email': [fake.email() for _ in range(500)],
    'Phone Number': [fake.phone_number() for _ in range(500)],
    'Address': [fake.address() for _ in range(500)],
})

print(users.head())

users.to_csv('users.csv', index=False)