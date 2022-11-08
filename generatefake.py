from faker import Faker
import random
import csv
import json

def generate(rows: int = 50, export: str['csv', 'json'] = 'csv', filename: str = 'clean'):
    """Generates fake registration or member data
    exports as csv or json"""
    fake = Faker()
    data = []
    for n in range(rows):
        per = {license:random.randint(1000, 9999), 'first': fake.first_name(), 'last': fake.last_name(), 'email': fake.email(),
               'phone': fake.phone_number(), 'address': fake.address(), 'city': fake.city(), 'state': fake.state(),
               'zip': fake.zipcode(), 'country': fake.country(), 'gender': random.choice(["M", "F"]),
               'category': random.choice(['CAT5', 'CAT3', 'MM60'])}
        data.append(per)
    if export=='csv':
        csv.DictWriter(open(f"{filename}.csv", 'w'), data[0].keys()).writerows(data)
    elif export=='json':
        with open(f"{filename}.json", "w") as final:
            json.dump(data, final)
