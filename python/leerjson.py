import requests
r = requests.get(url='https://api.github.com/users/ClauSaav/repos')
print(r.json())
