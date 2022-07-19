from django.test import TestCase

# Create your tests here.

import requests

url = 'https://api.github.com/users/jerit-baiju'
data = requests.get(url).json()

for x in data:
    print(f"{x} - {data[x]}")