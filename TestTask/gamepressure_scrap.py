import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime

def fetch_games(year: int, index: int):
    url = "https://www.gamepressure.com/ajax/gry-szukaj.asp"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "*/*",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "X-Requested-With": "XMLHttpRequest"
    }
    data = {
        "index": str(index),
        "dp": "0",
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
        release_date_raw = game.select("p.mb0")[-1].text.strip()
        
        # Convert release_date to the desired format
        try:
            release_date = datetime.strptime(release_date_raw, "%B %d, %Y").strftime("%Y-%m-%d")
        except ValueError:
            release_date = "Unknown"  # Handle cases where the date format is unexpected
        
        games.append({
            "name": name,
            "platforms": platforms,
            "genre": genre,
            "release_date": release_date
        })
    
    return games


# def fetch_games(year: int, index: int):
#     url = "https://www.gamepressure.com/ajax/gry-szukaj.asp"
#     headers = {
#         "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
#         "Accept": "*/*",
#         "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
#         "X-Requested-With": "XMLHttpRequest"
#     }
#     data = {
#         "index": str(index),
#         "dp": "0",
#         "dy": str(year),
#         "dm": "0",
#         "ds": "1",
#         "so": "0",
#         "st": "0",
#         "ss": "0",
#         "gp": "0",
#         "pl": "0",
#         "gk": "",
#         "gt": ""
#     }
    
#     response = requests.post(url, headers=headers, data=data)
#     if response.status_code != 200:
#         print("Ошибка запроса:", response.status_code)
#         return []
    
#     soup = BeautifulSoup(response.text, "html.parser")
#     games = []
    
#     for game in soup.select(".game-box-h-data"):
#         name = game.find_previous("h3").text.strip()
#         platforms = [img["alt"] for img in game.select(".cf.cf-gap5 img")]
#         genre = game.select_one("p.mb0 b").text.strip()
#         release_date = game.select("p.mb0")[-1].text.strip()
        
#         games.append({
#             "name": name,
#             "platforms": platforms,
#             "genre": genre,
#             "release_date": release_date
#         })
    
#     return games

def write_games_to_csv(games, filename):
    with open(filename, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["name", "platforms", "genre", "release_date"])
        if file.tell() == 0:  # Write header only if file is empty
            writer.writeheader()
        for game in games:
            writer.writerow({
                "name": game["name"],
                "platforms": ", ".join(game["platforms"]),
                "genre": game["genre"],
                "release_date": game["release_date"]
            })

if __name__ == "__main__":
    # games_2023 = fetch_games(2023, 1)
    # write_games_to_csv(games_2023, "data/GamePressure.csv")

    for year in range(2023, 2026):
        for index in range(51):
            print(f"{"*"*50}Fetching games for {year} - index {index}...")
            games = fetch_games(year, index)
            if games:  # Only write to CSV if games are fetched
                write_games_to_csv(games, f"data/GamePressure.csv")