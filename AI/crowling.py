import re
import requests
import statistics
import csv
import random
from bs4 import BeautifulSoup


def get_google_nutrient_effect(query):
    user_agents = [
    # Chrome for Windows
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",

    # Firefox for Windows
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:54.0) Gecko/20100101 Firefox/54.0",

    # Safari for Mac
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Safari/604.1.38"
    ]
    
    url = f"https://www.google.com/search?q={query}"
    headers = {"User-Agent": random.choice(user_agents)}
    res = requests.get(url, headers=headers)
    print(res)
    soup = BeautifulSoup(res.text, 'html.parser')
    result_stats = soup.find('div', {'class': 'LGOjhe'}).get_text()
    print(result_stats)
    
    return result_stats

dataset_name = []
dataset_effect = []

with open("nutrient_effect_v6.csv", "r", encoding = "utf-8") as f:
    wb = csv.reader(f)

    for line in wb:
        dataset_name.append(line[1])
        dataset_effect.append(line[2])

result = []
for idx, name in enumerate(dataset_name):
    print(idx, name)
    try:
        result.append(get_google_nutrient_effect(name+" 효능"))
    except:
        result.append("")