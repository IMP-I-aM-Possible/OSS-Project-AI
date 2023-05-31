import requests
import json
import pandas as pd

product_name_list = []
text_name_list = []

def nutrient_api():
    f = open("영양제2.txt", "r", encoding = "UTF-8")
    g = open("영양제.txt", "w", encoding = "UTF-8")
    text_data = f.readlines()

    for text in text_data:
        text = text.strip()
        text_name_list.append(text)

    dataset = {}
    url = 'http://openapi.foodsafetykorea.go.kr/api/a357bb13b7c84dd19dac/I2710/json/1/500'    # API 호출은 500개가 최대
    response = requests.get(url)
    contents = response.text

    json_ob = json.loads(contents)    #문자열을 json으로 변경
    #print(json_ob)
    #print(type(json_ob)) #json타입 확인 <class dict>

    body = json_ob['I2710']['row']

    # Dataframe으로 만들기
    dataframe = pd.json_normalize(body)

    for dict_key, dict_item in dataframe.items():
        dataset[dict_key] = dict_item

    for product_name in dataset['PRDCT_NM']:
        check = 0
        for idx, word in enumerate(product_name):
            if word == "(":
                product_name_list.append(product_name[0:idx])
                check = 1
                break
            else:
                continue
            
        if check != 1:
            product_name_list.append(product_name)
    count = 0

    for word_api in product_name_list:
        check = 0
        for word_text in text_name_list:
            if word_api == word_text:
                count += 1
                check = 1
        if check == 0:
            g.write(word_api + "\n")

    print(count)
    f.close()
    g.close()
    print("END")

nutrient_api()