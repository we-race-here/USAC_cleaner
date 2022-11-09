import csv
import datetime
import json
import random
from typing import Literal

from faker import Faker


def generate_data(rows: int = 50, export: Literal['csv', 'json'] = 'csv', filename: str = 'valid_data'):
    """Generates fake registration or member data
    exports as csv or json"""
    fake = Faker()
    data = []
    year = datetime.datetime.now().year
    for n in range(rows):
        per = {'license': random.randint(1000, 9999), 'First Name': fake.first_name(), 'Last Name': fake.last_name(),
               'email': fake.email(),
               'phone': fake.phone_number(), 'address': fake.address(), 'city': fake.city(), 'state': fake.state(),
               'zip': fake.zipcode(), 'country': fake.country(), 'gender': random.choice(["M", "F"]),
               'Birthdate': fake.date_of_birth(),
               'category': random.choice(['CAT5', 'CAT3', 'MM60'])}
        per.update({'Race Age': year - per['Birthdate'].year, 'Birthdate': per['Birthdate'].strftime('%d/%m/%Y')})
        data.append(per)
    if export == 'csv':
        with open(f"testdata/{filename}.csv", 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=data[0].keys())
            writer.writeheader()
            writer.writerows(data)
    elif export == 'json':
        with open(f"testdata/{filename}.json", "w") as final:
            json.dump(data, final)


def currupt_data(filename: str = 'valid_data', export: Literal['csv', 'json'] = 'csv'):
    """Takes a csv or json file and currupts it"""
    fake = Faker()
    fields = {'license': random.randint(1000, 9999), 'First Name': fake.first_name(), 'Last Name': fake.last_name(),
              'email': fake.email(),
              'phone': fake.phone_number(), 'address': fake.address(), 'city': fake.city(), 'state': fake.state(),
              'zip': fake.zipcode(), 'country': fake.country(), 'gender': random.choice(["M", "F"]),
              'Birthdate': fake.date_of_birth().strftime('%d/%m/%Y'),
              'category': random.choice(['CAT5', 'CAT3', 'MM60']),
              'Race_Age': random.randint(1, 100)}
    if export == 'csv':
        with open(f"testdata/{filename}.csv", 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            data = [row for row in reader]
    else:
        with open(f"testdata/{filename}.json", "r") as final:
            data = json.load(final)
    currupt = []

    for row in data:
        # print(f'currupting: {row}')
        if random.randint(0, 100) < 50:  # 50% chance of curruption
            random_field = random.choice(list(row.keys()))
            row[random_field] = '' if random.randint(0, 100) < 20 else fields[random_field]
        currupt.append(row)

    if export == 'csv':
        with open(f"testdata/{filename}_currupted.csv", 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=data[0].keys())
            writer.writeheader()
            writer.writerows(currupt)

if __name__ == '__main__':
    generate_data()
    currupt_data()
