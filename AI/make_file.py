import csv
import re

class getNutrientData:
    dataset_effect = []
    dataset_name = []
    product_name_list = []
    product_effect_list = []

    with open("nutrient_effect_v2.csv", "r", encoding="UTF8") as f:
        wb = csv.reader(f)
        count = 0
        for line in wb:
            dataset_name.append(line[1])
            dataset_effect.append(line[2])
    
    for product_name in dataset_name:    # 제품 이름에서 ()안에 있는거 지우기 ex)28-1029호
        check = 0
        for idx, word in enumerate(product_name):
            if word == "(":
                product_name_list.append(product_name[0:idx])
                check = 1
                break
            else:
                pass
        if check == 0:
            product_name_list.append(product_name)

    '''
    del_text = re.compile("\(국문\)|\(영문\)|[a-zA-Z]|[\t\n]")
    for product_effect in dataset_effect:
        product_effect_list.append(del_text.sub("", product_effect))
    '''
    del_text = re.compile("[^가-힣]")
    for product_effect in dataset_effect:
        product_effect_list.append(del_text.sub("", product_effect))
        
    with open("nutrient_effect_v3.csv", "w", newline='', encoding='UTF8') as f:
        wb = csv.writer(f)
        for i in range(len(product_effect_list)):
            wb.writerows([[i, product_name_list[i], product_effect_list[i]]])

    print("끝")
    
    
getNutrientData()