import requests
import json
import pandas as pd

class getNutrientData:
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