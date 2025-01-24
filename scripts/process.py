import requests
import pandas as pd
import csv
from io import BytesIO

def process():
    # Headers are [ 'Date', '... current', '... chained' ]
    yearl, quarterl = extract(levels)
    yearc, quarterc = extract(change)
    year = combine(yearl, yearc)
    quarter = combine(quarterl, quarterc)
    headers = ['date', 'level-current', 'level-chained', 'change-current', 'change-chained']
    writedata('year', headers, year)
    writedata('quarter', headers, quarter)

def combine(levels, change):
    # Combine levels and change data by column
    combined = [l + c[1:] for l, c in zip(levels, change)]
    return combined

def extract(url):
    response = requests.get(url)
    response.raise_for_status()
    
    # Read the Excel file into a pandas DataFrame
    xls_data = pd.ExcelFile(BytesIO(response.content))
    sheet = xls_data.sheet_names[0]  # Assuming data is in the first sheet
    df = xls_data.parse(sheet, header=None)

    # Remove headers and metadata rows, keeping only the data
    df = df.iloc[8:]  # Skip the first 8 rows (headers/metadata)
    df.reset_index(drop=True, inplace=True)

    # Separate annual and quarterly data
    annual = df.iloc[:, :3].dropna(how='any').values.tolist()
    annual = [[int(row[0])] + list(row[1:]) for row in annual if pd.notnull(row[0])]

    quarterly = df.iloc[:, 4:7].dropna(how='any').values.tolist()
    
    # Fix quarterly date format (e.g., 1947Q1 to 1947-01-01)
    def fix_quarters(date):
        mapping = {
            'Q1': '-01-01',
            'Q2': '-04-01',
            'Q3': '-07-01',
            'Q4': '-10-01'
        }
        for key, value in mapping.items():
            date = date.replace(key, value)
        return date

    quarterly = [[fix_quarters(str(row[0]))] + row[1:] for row in quarterly]

    return annual, quarterly

def writedata(name, headers, data):
    with open(f'data/{name}.csv', 'w', newline='') as fo:
        writer = csv.writer(fo)
        writer.writerow(headers)
        writer.writerows(data)

if __name__ == '__main__':
    levels = 'https://apps.bea.gov/national/xls/gdplev.xlsx'
    change = 'https://apps.bea.gov/national/xls/gdpchg.xlsx'
    process()
