import openai
import time
import pandas as pd
import re
import random
import papago

API_KEY = ""
openai.api_key = API_KEY
gpt_answer = []

def gptTest(question):
    start = time.time()
    instruction_message_list = [
        "You are a doctor. ",
        "Understand [Questions] and prepare answers to those questions.",
        "You must recommend nutrients related to [question]",
        "[Question] If you're not feeling well, you recommend foods, nutrients, and nutritional supplements to help you improve.",
        "[Question] If it is not health-related, we cannot answer it.' I'm sorry.'",
        "We combine the answers and answer them as if the doctor were making a diagnosis."
    ]
    e_question = papago.ko_to_en(question)
    if gpt_answer:
        completion = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo",
        messages = [
            {"role":"system", "content": "".join(instruction_message_list)},
            {"role":"assistant", "content": gpt_answer[-1]},
            {"role":"user", "content": e_question}
        ],
        temperature=0.5,
        max_tokens=2000,
        top_p=0.6,
        frequency_penalty=0,
        presence_penalty=0
        )
    else:
        completion = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo",
        messages = [
            {"role":"system", "content": "".join(instruction_message_list)},
            {"role":"user", "content": e_question}
        ],
        temperature=0.5,
        max_tokens=2000,
        top_p=0.6,
        frequency_penalty=0,
        presence_penalty=0
        )
    result = papago.en_to_ko(completion.choices[0].message.content)
    #result = (completion.choices[0].message.content)
    end = time.time()
    print(f"'{question}' 답변 완료({end-start}초)")
    
    if search_excel(result):
        result += "\n\n추천 영양제\n" + str("\n".join(search_excel(result)))
    else:
        result += "\n\n해당 증상에 추천되는 영양제가 사이트에 존재하지 않습니다.\n"
    gpt_answer.append(result)
    
    return result

def data_cutting(nutrient_data, type):
    yeye = nutrient_data    # 영양소 삽입
    for idx, bunch in enumerate(nutrient_data):
        sample = []
        for word in bunch:
            word = re.sub(" ", "", word)
            word = re.sub("\.", "", word)
            word = re.sub(",", "", word)
            word = re.sub('"', "", word)
            word = re.sub("-", "", word)
            word = re.sub(":", "", word)
            word = re.sub("☆|♦", "", word)
            word = re.sub("\{|\}", "", word)
            word = re.sub("\(|\)", "", word)
            word = re.sub("피부|치아|알코올|단일불포화지방|고도불포화지방|불포화지방", "", word)
            word = re.sub("공급|다중|함유|지방산|세지방의|열매|오일|씨|발효|수지|유기농|추출물|분말|총|®|약", "", word)
            word = re.sub(r"채소|콜레스테롤|칼로리|지방|탄수화물|탄수화물|단백질|당류|포화|의|에서", "", word)
            word = re.sub(r'\([^)]*\)', "", word)
            word = re.sub(r'\d+[a-zA-Z]+', "", word)
            word = re.sub(r'\d+\.\d+[a-zA-Z]+', "", word)
            word = re.sub("\d+", "", word)
            if type == 0:
                word = re.sub(r"[a-zA-Z]", "", word)
                word = re.sub("비타민", "", word)
                
            if len(word) > 0 and word != ": ":
                sample.append(word)
        yeye[idx] = sample
    return yeye

def recommend_pill(nutrient_data, gpt_answer, excel_data):
    recommend = []
    count = 0
    test = []
    
    while(len(recommend) != 5):
        if count == 5:
            break
        already_recommend = []
        for idx, nutrient in enumerate(nutrient_data):
            for name in nutrient:
                name = name.strip()
                if "밀크시슬" in name:
                    name = re.sub("밀크시슬", "밀크 씨슬", name)
                if name in gpt_answer and len(name) > 1 and excel_data["name"][idx] not in recommend:
                    #print(name, nutrient_data[idx], idx)
                    already_recommend.append(name)
                    recommend.append(excel_data["name"][idx])
        count+=1
    return recommend

def search_excel(gpt_answer):
    recommend = []
    core_recommend_pill = []
    sub_recommend_pill = []
    core_nutrient_data = []
    sub_nutrient_data = []
    count = 0
    
    excel_data = pd.read_excel("./excel/ossexcel2.xlsx", usecols=[2, 10, 11], names = ["name", "core_nutrient", "sub_nutrient"])
    for i in range(len(excel_data)):
        #nutrient_data.append(excel_data["nutrient"][i][1:-1].split('"'))
        sub_nutrient_data.append(excel_data["sub_nutrient"][i].split(','))
        core_nutrient_data.append(excel_data["core_nutrient"][i].split(','))
    
    sub_nutrient_data = data_cutting(sub_nutrient_data, 0)
    core_nutrient_data = data_cutting(core_nutrient_data, 1)
    
    gpt_answer = re.sub("비타민 ", "비타민", gpt_answer)
    core_recommend_pill = recommend_pill(core_nutrient_data, gpt_answer, excel_data)
    sub_recommend_pill = recommend_pill(sub_nutrient_data, gpt_answer, excel_data)
    
    #print(len(core_recommend_pill), len(sub_recommend_pill))
    
    while(len(recommend) != 5):
        try:
            nutritional_supplements = random.choice(core_recommend_pill)
            if nutritional_supplements not in recommend:
                recommend.append(nutritional_supplements)
        except:
            pass
        if len(recommend) == 5 or count == 6:
            break
        try:
            nutritional_supplements = random.choice(sub_recommend_pill)
            if nutritional_supplements not in recommend:
                recommend.append(nutritional_supplements)
        except:
            pass
        count += 1
        
    return recommend