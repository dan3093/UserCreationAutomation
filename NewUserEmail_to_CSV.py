from imap_tools import MailBox, A
from passwordgenerator import pwgenerator
from functions import *
from bwimport import bwcreate
from platform import node, system
import csv
import subprocess

# mailbox settings
mailbox = MailBox('imap.mail.com')
mailbox.login('user@example.com', 'password', initial_folder='New Users')

# Look for unread new user request emails from HR
query = A(subject='New User Request', from_="hr@example.com", answered=False)

msg = []
clean_msg = []
dict_data = []
dictionary = {}
uname = ''
emailadd = ''
OU = ''

print('             ### Starting Script ### \n\n### Checking user@example.com "New Users" folder ###')

# fetch new user request emails > append to list > remove whitespace, new lines, etc. from list items.
number_of_messages = 0

for msgs in mailbox.fetch(query):
    msg = msgs.text
    msg = msg.replace('>', '')
    msg = msg.replace('\r', '')
    msg = msg.replace('<br/', '')
    msg = msg.split('\n')
    number_of_messages += 1

    # check for/remove blank items in list
    for x in msg:
        if x == '':
            msg.remove(x)

    for x in msg:
        x = x.strip()
        clean_msg.append(x)

    # create dictionary from list
    dictionary = list_to_dict(clean_msg)

    # remove whitespace from key values
    dictionary = strip_dict_whitespace(dictionary)

    # add username column to dictionary
    uname = username(dictionary)
    dictionary['username'] = uname

    # add email column to dictionary
    emailadd = create_email(uname, dictionary)
    dictionary['emailaddress'] = emailadd

    # Generate easy to read/but also secure temporary password
    password = pwgenerator.pw(8, 9, 10000, 2)
    dictionary['password'] = password

    # Set OU for user to be created in
    OU = selectou(dictionary)
    dictionary['OU'] = OU

    # Append each NewUser Dictionary to a list
    dict_data.append(dictionary)

if number_of_messages > 0:
    print(
        f"    {number_of_messages} New users found!\n\n### Creating scriptable import files from information in email request ###\n\n### Importing User Credentials to Bitwarden ###\n\n### Creating Users in Active Directory###\n\n")
else:
    print(
        "    No new user requests found! \n    Please check the user@example.com email account in 'New Users' folder.\n")

# Write dict_data list to CSV
csv_columns = ['First name', 'Last Name', 'Extension', 'Direct Number', 'Fax Number', 'Cell Number', 'Desk Location',
               'Job title', 'Hire Date', 'Role', 'Department', 'Location', 'Company', 'Needs Key FOB',
               'Software Needed', 'Comments', 'username', 'emailaddress', 'password', 'OU']
csv_file_all = "newusers.csv"
csv_file_company1 = "newusers_company1.csv"
csv_file_company2 = "newusers_company2.csv"

# Write New User CSV
try:
    with open(csv_file_all, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
        writer.writeheader()
        try:
            for data in dict_data:
                writer.writerow(data)
        except IOError:
            print("ERROR: Unable to write data to CSV.")
except IOError:
    print("I/O Error - Close CSV if Open")

# Write Company1 New User CSV
try:
    with open(csv_file_company1, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
        writer.writeheader()
        try:
            for data in dict_data:
                if data["Company"] == "Company1":
                    writer.writerow(data)
        except IOError:
            print("ERROR: Unable to write data to CSV.")
except IOError:
    print("I/O Error - Close CSV if Open")

# Write Network New User CSV
try:
    with open(csv_file_company2, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
        writer.writeheader()
        try:
            for data in dict_data:
                if data["Company"] == "Company2":
                    writer.writerow(data)
        except IOError:
            print("ERROR: Unable to write data to CSV.")
except IOError:
    print("I/O Error - Close CSV if Open")

mailbox.move(mailbox.uids(), 'New Users Completed')

mailbox.logout()

# create bitwarden import file

bwcreate()


# import bitwarden import file

if system() == "Linux":
    subprocess.call(['sh', './bitwardenimport.sh'])
elif system() == "Windows":
    subprocess.call(["powershell.exe", r'.\bitwardenimport.ps1'])
else:
    pass

# Restrict Script to only run on specific DC or computer.

dcname = node()

if dcname == "Company1-DC":
    subprocess.call(["powershell.exe", r'.\AutomateUserCreation_Company1.ps1'])
elif dcname == "Company2-DC":
    subprocess.call(["powershell.exe", r'.\AutomateUserCreation_Company2.ps1'])
else:
    print(f"Error! -- Active Directory script cannot be run on this host: {dcname}")
print("### Script Finished ###")
