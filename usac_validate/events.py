from datetime import datetime
from time import timezone

import requests


def events(*args, **options):
    years = options.get('years')
    if not years:
        years = [timezone.now().year]
    for year in years:
        start_date = datetime.date(year, 1, 1)
        end_date = start_date.replace(year=year + 1) - datetime.timedelta(days=1)
    res = requests.get(
        f'https://laravel-api.usacycling.org/api/v1/event_search?start_date={start_date}&end_date={end_date}')
    if not res.ok:
        res.raise_for_status()
    data = res.json().get("data") or []
    return data
