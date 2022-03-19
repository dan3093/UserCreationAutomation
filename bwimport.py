import csv
from csv import DictWriter

csv_columns_bwimport = ['collections', 'type', 'name', 'notes', 'fields', 'reprompt', 'login_uri', 'login_username', 'login_password', 'login_totp']
csv_file = "newusers.csv"


list1 = []


def bwcreate():
    try:
        with open(csv_file, "r", newline='') as infile, open("bwimport.csv", "w", newline='') as outfile:
            reader = csv.DictReader(infile)
            writer: DictWriter[str] = csv.DictWriter(outfile, fieldnames=csv_columns_bwimport)

            for row in reader:
                dictobject = {"type": "login", "name": (row['First name'] + ' ' + row['Last Name']),
                              "login_username": row['username'], "login_password": row['password']}
                # dictobject["collections"] = "New User Import"
                list1.append(dictobject)

            writer.writeheader()
            writer.writerows(list1)

    except IndexError:
        pass
