import requests


TOKEN = '08defa01e3bd4e8b6aad21c4b16e3cc822a665f6'

url = 'https://api-ssl.bitly.com/v4/user'
headers = {'Authorization': 'Bearer 08defa01e3bd4e8b6aad21c4b16e3cc822a665f6'}
response = requests.get(url, headers=headers)
response.raise_for_status()
for key, value in response.json().items():
    print("{0}: {1}".format(key,value))
