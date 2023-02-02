import json

import requests
def usac_clubs(path=None):
    # res = requests.get('https://laravel-api.usacycling.org/api/v1/club_search/1/')
    # res = requests.get('https://usacycling.org/API/clubs/')
    # res = requests.get("https://usacycling.org/API/clubs/?state=CO&radius=5&limit=999")
    all_clubs = requests.get("https://usacycling.org/API/clubs/?limit=9999")
    clubs = {}
    if not all_clubs.ok:
        all_clubs.raise_for_status()
    clubs['all'] = all_clubs.json()

    highschool = requests.get("https://usacycling.org/API/clubs/?org=High%20School&radius=5&limit=999")
    if not highschool.ok:
        highschool.raise_for_status()
    clubs['highschool'] = highschool.json()

    usac = requests.get("https://usacycling.org/API/clubs/?org=USAC&radius=5&limit=9999")
    if not usac.ok:
        usac.raise_for_status()
    clubs['usac'] = usac.json()

    collegiate = requests.get("https://usacycling.org/API/clubs/?org=Collegiate&radius=5&limit=999")
    if not collegiate.ok:
        collegiate.raise_for_status()
    clubs['collegiate'] = collegiate.json()

    uspro = requests.get("https://usacycling.org/API/clubs/?org=USPRO&radius=5&limit=999")
    if not uspro.ok:
        uspro.raise_for_status()
    clubs['uspro'] = uspro.json()

    if path is not None:
        with open('../clubs.json', 'w') as f:
            json.dump(clubs, f)
    return clubs
