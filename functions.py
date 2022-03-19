dictionary = {}


# create dictionary from list
def list_to_dict(listobject):
    for item in listobject:
        key, value = item.split(':')
        dictionary[key] = value
    return dictionary


# remove whitespace from key values
def strip_dict_whitespace(d):
    return {key.strip(): value.strip()
            for key, value in d.items()}


# create username
def username(dictobject):
    fname = dictobject["First name"]
    lname = dictobject["Last Name"]
    uname = (fname[:1] + lname).lower()
    if len(uname) > 11:
        uname = uname[0:11]
    return uname


def selectou(dictobject):
    ou = ''
    if dictobject['Company'] == "Company1":
        ou = "OU=Users,DC=company1,DC=com"
    if dictobject['Company'] == "Company2":
        ou = "OU=Users,DC=company2,DC=com"
    if dictobject['Company'] == "Other":
        ou = ""
    return ou


# create email address
def create_email(uname, dictobject):
    emailaddress = ''
    if dictobject['Company'] == "Company1":
        emailaddress = str(uname) + '@company1.com'
    if dictobject['Company'] == "Company2":
        emailaddress = str(uname) + '@company2.com'
    return emailaddress
