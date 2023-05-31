import requests
import csv
import math
import numpy as np
import matplotlib.pyplot as plt
import statistics
from sklearn.preprocessing import MinMaxScaler
from bs4 import BeautifulSoup

nutrient_name = []
search_count = []
dataset_effect = []
dataset_name = []

def awareness_score(x):
    return math.log(math.log(x))

def get_google_search_count(query):
    url = f"https://www.google.com/search?q={query}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36'}
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser')
    result_stats = soup.find(id="result-stats").get_text()
    count = ''.join([num for num in result_stats if num.isdigit()])
    return int(count)

with open('nutrient_effect_v3.csv', 'r', encoding='utf-8') as f:
    wb = csv.reader(f)

    for line in wb:
        dataset_name.append(line[1])
        dataset_effect.append(line[2])
        nutrient_name.append(line)

search_count = []
for search in nutrient_name:
    count = get_google_search_count(search[1])
    search_count.append(count)
    print(search[0], count)

for i in range(0,399):
    if search_count[i] > 35400001045:
        count +=1
        search_count[i] = 15400001045

scaler = MinMaxScaler()
search_count_np = np.array(search_count)
scaled_data = scaler.fit_transform(search_count_np.reshape(-1, 1))

#print((np.ceil(scaled_data[0]*1000)/100))
scaled_data_plus = []
for i in range(len(search_count)):
    scaled_data_plus.append((np.ceil(scaled_data*1000)/1000))

plt.plot(range(0,399), scaled_data_plus[0])
plt.show