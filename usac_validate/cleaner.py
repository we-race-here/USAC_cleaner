import csv
import json
from typing import Literal

import pandas as pd
from Levenshtein import distance
from thefuzz import process

from notebooks.config import event_corrected_fields
from notebooks.config import event_invalid_fields
from notebooks.config import usac_upload_fields


def load_usac_master(usac_master: str) -> tuple[pd.DataFrame, list[dict, ...], list[str, ...]]:
    """Expects the unmodified promoter CSV file downloaded from USAC"""
    usac_master_df = pd.read_csv(usac_master)
    usac_master_dict = usac_master_df.to_dict(orient='records')
    usca_licenses = usac_master_df['License #'].tolist()
    return usac_master_df, usac_master_dict, usca_licenses


def load_event_file(event_file):
    """Expects a CSV or excel file"""
    if event_file.endswith('.csv'):
        with open(event_file, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            data = [row for row in reader]
    elif event_file.endswith('.xlsx'):
        data = pd.read_excel(event_file).to_dict(orient='records')
    else:
        raise ValueError('Invalid file type')
    return data

def fuzzy_match(sample, match_list):
    """Fuzzy matches a sample string to a list of strings"""
    return process.extractOne(sample, match_list)


class UsacDataValidater(object):
    def __init__(self, usac_master: str, event_file: str, filetype):
        self.unknown_fields: list[dict, ...] = []
        self.corrected_cols: list[dict, ...] = []
        self.invalid_fields: list[dict, ...] = []
        self.usac_master_df, self.usac_master_dict, self.usac_licenses = load_usac_master(usac_master)
        self.event_data: list[dict, ...] = load_event_file(event_file)
        self.filetype: Literal['entries', 'results'] = filetype

    def upload_fields(self) -> tuple[list[dict, ...], list[dict, ...], list[dict, ...]]:
        """Validate file for upload to USAC"""
        self.corrected_cols: list[dict, ...] = []
        self.unknown_fields: list[dict, ...] = []
        for col in self.event_data[0].keys():  # Check each field
            if col in usac_upload_fields:  # Good field names
                self.corrected_cols.append({col: (col, 'correct')})
            elif col in event_corrected_fields.keys():  # correctable field names
                self.corrected_cols.append({col: (event_corrected_fields[col], 'Corrected')})
            elif col in event_invalid_fields.keys():  # invalid field names with recomendations
                self.invalid_fields.append({col: (event_invalid_fields[col], 'Invalid')})
            else:  # unknown field names
                self.unknown_fields.append({col: ('Unknown', 'Unknown')})
        return self.invalid_fields, self.corrected_cols, self.unknown_fields

    def team_name(self, fuzzy=True):
        """Check the rider team name against the USAC master list"""
        with open('../tests/testdata/team_club_collegiate_highschool_USAC.json', 'r') as f:
            teams = json.load(f)
            print(f"Teams count: {len(teams)}")
        team_names = [str(team['name'].lower()) for team in teams]
        corrected = []
        for rider in self.event_data:
            if rider['Team'].lower() in team_names:
                corrected.append({rider['Team'], 'correct'})
            elif rider['Team'] == '':
                corrected.append({rider['Team'], 'missing'})
            elif not fuzzy:
                if rider['Team'] not in ['', 'None', 'none', 'N/A', 'n/a', 'NA', 'na', 'nan', 'Nan', 'NAN']:
                    try:
                        suggestion = min(team_names, key=lambda x: distance(
                                x.replace('cycling', '').replace('team', '').replace('club', '').replace(' ', ''),
                                rider['Team'].lower().replace('cycling', '').replace('team', '').replace('club',
                                                                                                     '').replace(' ',
                                                                                                                 '')
                        ))
                        corrected.append({rider['Team'], ('suggestion', suggestion)})
                        print({rider['Team']: ('suggestion', suggestion)})
                    except:
                        print(f"Error with: {rider['Rider']}, {rider['Team']}")
                        corrected.append({rider['Team'], ('suggestion', 'ERROR')})
            elif fuzzy:
                if rider['Team'] not in ['', 'None', 'none', 'N/A', 'n/a', 'NA', 'na', 'nan', 'Nan', 'NAN']:
                    try:
                        suggestion = process.extract(rider['Team'], team_names, limit=3)
                        print(f"searching for: {rider['Team']}")
                        print(f"Suggestion: {suggestion}")
                        corrected.append({rider['Team'], ('suggestion', suggestion)})
                    except:
                        print(f"Error with: {rider['Rider']}, {rider['Team']}")
                        corrected.append({rider['Team'], ('suggestion', 'ERROR')})

        return self.event_data[0]['Team']
