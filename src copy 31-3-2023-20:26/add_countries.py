import csv
from db import ow_db
from sqlalchemy.sql import text

def get_country_tuples():
    countries_list = []
    with open('../Data/countries.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            # Extract the values from the row
            code = row[0]
            name = row[1]
            countries_list.append((code, name))
    
    return countries_list

def insert_countries():
    for tuple in get_country_tuples():
        sql = text('INSERT INTO countries (code, name) VALUES (:code, :name)')
        ow_db.session.execute(sql, {"code":tuple[0], "name":tuple[1]})
        ow_db.session.commit()
        
    print("Countries inserted into table")