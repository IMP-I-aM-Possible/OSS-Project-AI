import random
import json
import urllib.request

api_key_list = []

rand_choice = random.choice(api_key_list)
client_id = rand_choice[0] # 개발자센터에서 발급받은 Client ID 값
client_secret = rand_choice[1] # 개발자센터에서 발급받은 Client Secret 값

def ko_to_en(text):
    encText = urllib.parse.quote(text)
    data = "source=ko&target=en&text=" + encText
    url = "https://openapi.naver.com/v1/papago/n2mt"
    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id",client_id)
    request.add_header("X-Naver-Client-Secret",client_secret)
    response = urllib.request.urlopen(request, data=data.encode("utf-8"))
    rescode = response.getcode()
    if(rescode==200):
        response_body = response.read()
        result = response_body.decode('utf-8')
        translate_text = json.loads(result)
        return(translate_text['message']['result']['translatedText'])
    else:
        print("Error Code:" + rescode)

def en_to_ko(text):
    kocText = urllib.parse.quote(text)
    data = "source=en&target=ko&text=" + kocText + "&honorific=true"
    url = "https://openapi.naver.com/v1/papago/n2mt"
    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id",client_id)
    request.add_header("X-Naver-Client-Secret",client_secret)
    response = urllib.request.urlopen(request, data=data.encode("utf-8"))
    rescode = response.getcode()
    if(rescode==200):
        response_body = response.read()
        result = response_body.decode('utf-8')
        translate_text = json.loads(result)
        return(translate_text['message']['result']['translatedText'])
    else:
        print("Error Code:" + rescode)