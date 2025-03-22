import json
import requests
import pandas as pd

def request_api(offset):
    # Формируем URL с учетом пагинации
    url = f'https://vginsights.com/api/v1/games?gameTypes=10,20&released=&exclude_gameTypes=30&limit=20&offset={offset}&sortOrder=-1&sortField=released&isGamePageRequest=true&platforms=steam'
    return url


headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:136.0) Gecko/20100101 Firefox/136.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJ2Z2luc2lnaHRzLmNvbSIsInZnaVZlcnNpb24iOjEuMzEsInRpbWUiOjE3NDI2NDI5NTM4MjMsInByb2ZpbGUiOnsiaWQiOiIxMDcwOTc4OTM3MDAwMjU4MDA0NDIiLCJlbWFpbCI6InNpcml1c2JsYWM3QGdtYWlsLmNvbSJ9LCJhY2Nlc3MiOnsibGV2ZWwiOjEwfSwibWV0YSI6eyJoYXNBY3RpdmVTdHJpcGVTdWIiOmZhbHNlLCJoYXNBY3RpdmVQYXRyZW9uU3ViIjpmYWxzZSwiaXNGcmVlVHJpYWxBbGxvd2VkIjp0cnVlLCJpc1VzZXJPbkZyZWVUcmlhbCI6ZmFsc2V9LCJpYXQiOjE3NDI2NDI5NTMsImV4cCI6MTc0NjI3MTc1M30.fyuzrv3dnj8x6nsbBTANH-MO2Jsd0KowaKI3yvBkQjM',
    "Sec-Fetch-User": "?1",
    "Connection": "keep-alive",
    "Cookie": 'g_state={"i_l":0}'
}


all_games_data = []
offset = 0
limit = 500

# Перебор пагинации с шагом 20
while offset < limit:
    url = request_api(offset)
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        print(f"Ошибка: {response.status_code} на offset={offset}")
        break

    games_data = response.json().get("rows", [])
    
    if not games_data:
        print(f"Достигнут конец данных на offset={offset}")
        break

    # Фильтруем инди-игры
    filtered_games = [
        game for game in games_data
        if "Indie" not in game.get("genres", "") and game.get("publishers_type", "").lower() != "indie"
    ]

    all_games_data.extend(filtered_games)
    print(f"Обработано {len(filtered_games)} записей на offset={offset}")

    offset += 20
    
df = pd.DataFrame(all_games_data)

df.to_csv('games_data.csv', index=False, encoding='utf-8')

print(f"Данные успешно записаны в games_data.csv. Всего записей: {len(all_games_data)}")