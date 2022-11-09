import csv
import json
from typing import Literal
import pandas as pd

from config import usac_master_fields
from config import usac_upload_fields
from config import event_corr_fields


def clean_data(filename: str):
    if filename.endswith('.csv'):
        with open(filename, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            data = [row for row in reader]
    elif filename.endswith('.json'):
        with open(filename, "r") as final:
            data = json.load(final)
    else:
        raise ValueError('Invalid file type')
    return data


def check_fields(data: list[dict, ...]):
    """Checks for missing fields or incorrect """
    data[0].keys()


class Usac_Data_Cleaner(object):

    def __init__(self, usac_master: str, event_file: str, filetype: Literal['entries', 'results']):
        self.usac_master_df, self.usac_master_dict, self.usca_licenses = self.load_usac_master(usac_master)
        self.event_data = self.load_event_file(event_file)
        self.filetype = filetype

    def load_usac_master(self, usac_master):
        """Expects the unmodified promoter CSV file downloaded from USAC"""
        usac_master_df = pd.read_csv(usac_master)
        usac_master_dict = usac_master_df.to_dict(orient='records')
        usca_licenses = usac_master_df['License #'].tolist()
        return usac_master_df, usac_master_dict, usca_licenses

    def load_event_file(self, event_file):
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

    def check_fields(self):
        """Checks for missing fields or incorrect field names"""
        event_corrected_fields = []
        for row in self.event_data:
            corrected_row = {}
            for field in row.keys():
                if field in usac_master_fields:
                    corrected_row[usac_master_fields[field]] = row[field]
                else:
                    corrected_row[field] = row[field]
            event_corrected_fields.append(corrected_row)
        self.event_data = event_corrected_fields
        event_fields = self.event_data[0].keys()
        field_name_corrections = []
        for f in event_fields:
            if f not in usac_master_fields:
                if f in event_corr_fields.keys():
                    corrected = event_corr_fields[f]
                field_name_corrections.append({f: corrected})
            else:
                field_name_corrections.append({corrected: 'Unknown'})
        return field_name_corrections


