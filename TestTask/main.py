# import requests
# from bs4 import BeautifulSoup
# import time

# def parse_games(status: int, max_pages: int = 10):
#     url = "https://www.gamepressure.com/ajax/gry-szukaj.asp"
    
#     headers = {
#         "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:136.0) Gecko/20100101 Firefox/136.0",
#         "Origin": "https://www.gamepressure.com",
#         "Referer": "https://www.gamepressure.com/games/search/",
#         "Content-Type": "application/x-www-form-urlencoded",
#         "Cookie": "ASPSESSIONIDQGBCSQRR=NMKPDIOCIMPJFPCKJKGILIOJ"
#     }

#     all_games = []
    
#     for page in range(1, max_pages + 1):
#         data = {
#             "status": status,  # 0 - Released, 1 - Upcoming
#             "page": page,
#             "sort": "date",    # Параметр сортировки
#             "platform": "all"  # Фильтр платформ (может потребоваться уточнение)
#         }

#         try:
#             response = requests.post(
#                 url, 
#                 headers=headers, 
#                 data=data, 
#                 timeout=10
#             )
#             response.raise_for_status()
            
#             # Парсинг HTML-ответа
#             soup = BeautifulSoup(response.text, "html.parser")
            
#             # Пример парсинга (настройте под структуру сайта)
#             games = soup.select(".game-item")
#             if not games:
#                 print(f"Страница {page} пустая")
#                 break  # Прекращаем если страницы пустые
                
#             for game in games:
#                 title = game.select_one(".title").text.strip()
#                 platform = game.select_one(".platform").text.strip()
#                 release_date = game.select_one(".date").text.strip()
                
#                 all_games.append({
#                     "title": title,
#                     "platform": platform,
#                     "release_date": release_date,
#                     "status": "Released" if status == 0 else "Upcoming"
#                 })

#             time.sleep(1.5)  # Задержка против блокировки

#         except Exception as e:
#             print(f"Ошибка на странице {page}: {str(e)}")
#             break

#     return all_games

# # Сбор данных
# released = parse_games(status=0)  # Выпущенные игры
# upcoming = parse_games(status=1)  # Предстоящие игры

# # Объединение результатов
# all_games = released + upcoming

import requests
from bs4 import BeautifulSoup
 
# Define your target URL
url = 'https://www.gamepressure.com/games/kingdom-come-deliverance-ii/z369b2'
 
# Send an HTTP GET request and fetch the HTML content
response = requests.get(url)
 
# Fetch the HTML content
html_content = response.text
print(response.status_code)
    
# Parse the HTML content using Beautiful Soup
soup = BeautifulSoup(html_content, 'html.parser')
    
# Print formatted HTML content
# print(soup.prettify())
