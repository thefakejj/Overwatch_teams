import csv


with open("countries.csv") as file:
    reader = csv.reader(file, delimiter=',')
    for row in reader:
        row = row[1:]
        with open("countries2.csv", "a") as new:
            new.write(f"row[0], row[1]")

