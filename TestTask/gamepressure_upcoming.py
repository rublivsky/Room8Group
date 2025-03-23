import requests
from bs4 import BeautifulSoup
from gamepressure_scrap import write_games_to_csv
import csv

def fetch_games(index: int, year: int = 0, dp: int = 1):
    url = "https://www.gamepressure.com/ajax/gry-szukaj.asp"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "*/*",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "X-Requested-With": "XMLHttpRequest"
    }
    data = {
        "index": str(index),
        "dp": str(dp),
        "dy": str(year),
        "dm": "0",
        "ds": "1",
        "so": "0",
        "st": "0",
        "ss": "0",
        "gp": "0",
        "pl": "0",
        "gk": "",
        "gt": ""
    }
    
    response = requests.post(url, headers=headers, data=data)
    if response.status_code != 200:
        print("Ошибка запроса:", response.status_code)
        return []
    
    soup = BeautifulSoup(response.text, "html.parser")
    games = []
    
    for game in soup.select(".game-box-h-data"):
        name = game.find_previous("h3").text.strip()
        platforms = [img["alt"] for img in game.select(".cf.cf-gap5 img")]
        genre = game.select_one("p.mb0 b").text.strip()
        release_date = game.select("p.mb0")[-1].text.strip()
        
        games.append({
            "name": name,
            "platforms": platforms,
            "genre": genre,
            "release_date": release_date
        })
    
    return games

# Пример использования
if __name__ == "__main__":
    index = 0
    while True:
        games_data = fetch_games(index)
        if not games_data:  # Stop if no games are fetched
            break
        write_games_to_csv(games_data, "data/GamePressureUpcoming.csv")
        index += 1
