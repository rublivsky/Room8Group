import requests

url = 'https://vginsights.com/games-database?gameTypes=10,20&released=&exclude_gameTypes=30'

response = requests.get(url)

print(response.text)