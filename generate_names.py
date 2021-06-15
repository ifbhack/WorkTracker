# API used: https://www.back4app.com/database/back4app/list-of-names-dataset

import json
import urllib
import requests
from random import *

url = 'https://parseapi.back4app.com/classes/NamesList?skip=0&limit=25000&keys=Name'
headers = {
    'X-Parse-Application-Id': 'zsSkPsDYTc2hmphLjjs9hz2Q3EXmnSxUyXnouj1I', # This is the fake app's application id
    'X-Parse-Master-Key': '4LuCXgPPXXO2sU5cXm6WwpwzaKyZpo3Wpj4G4xXK' # This is the fake app's readonly master key
}
data = json.loads(requests.get(url, headers=headers).content.decode('utf-8')) # Here you have the data that you need
test = json.dumps(data, indent=2)

names = []

for each in range(25):
    random_name = data['results'][randint(1, 6000)]['Name']
    random_surname = data['results'][randint(1, 6000)]['Name']
    names.append([random_name, random_surname])

print(names)
