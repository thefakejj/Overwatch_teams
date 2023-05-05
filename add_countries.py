import csv
from sqlalchemy.sql import text

def get_country_tuples():
    countries_list = []
    with open('./Data/countries.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            code = row[0]
            code = code.lower()
            name = row[1]
            countries_list.append((code, name))
    
    return countries_list

def insert_countries(database):
    for tuple in get_country_tuples():
        sql = text('INSERT INTO countries (code, name) VALUES (:code, :name)')
        database.session.execute(sql, {"code":tuple[0], "name":tuple[1]})
        database.session.commit()
        
    print("Countries inserted into table")