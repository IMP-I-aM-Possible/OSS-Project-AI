import numpy as np
import csv
from sentence_transformers import SentenceTransformer
import faiss

dataset_name = []    # csv 파일에 저장한 영양소 이름
dataset_effect = []    # csv 파일에 저장한 영양소 효능

with open("./csv/nutrient_effect_pc_v2.3.csv", "r", encoding = "utf-8") as csv_file:    # csv file open    번호, 이름, 효능
    wb = csv.reader(csv_file)
    for line in wb:
        dataset_name.append(line[1])    
        dataset_effect.append(line[2])

model = SentenceTransformer('jhgan/ko-sroberta-multitask')    # Bert모델 로드
encoded_data = model.encode(dataset_effect)    # 영양소 효능을 위에서 로드한 Bert로 인코딩

# faiss.IndexFlatIp는 cos_sim을 구해주는 faiss 함수 768은 차원을 말함
# faiss.IndexIDMap는 각 벡터에 대해 고유한 ID를 매핑하는 인덱스
# faiss.add_with_ids는 벡터와 해당 벡터의 ID를 인덱스에 추가, 첫번째 인자는 벡터 배열 두번째 인자는 ID 배열
index = faiss.IndexIDMap(faiss.IndexFlatIP(768))
index.add_with_ids(encoded_data, np.array(range(0, len(dataset_effect))))

#faiss.write_index(index, 'nutrient_effect_data')

def search(query):
    result = []    # 추천되는 영양소 이름 저장
    recomend_idx = []    # 추천되는 영양소의 인덱스 번호
    score_idx_name_list = []    # 영양소의 인덱스 별 유사도 점수 저장
    intergrade = []    # 중간저장단계
    need_idx = []
    
    k = 20
    query_vector = model.encode([query])    # Beart 모델로 벡터화
    top_k = index.search(query_vector, k)   # faiss를 사용해서 쿼리벡터에서 높은 값 10개 추출
    
    for list_idx, idx in enumerate(top_k[1].tolist()[0]):
        #print(top_k[0][0][list_idx], idx, dataset_name[idx])  # 유사도 높은 영양소의 점수, 인덱스, 이름
        if dataset_name[idx] not in intergrade and top_k[0][0][list_idx] >= 40 and len(need_idx) < 5:
            #intergrade.append([top_k[0][0][list_idx], idx, dataset_name[idx]])    # 점수, 인덱스, 이름 순으로 리스트에 저장
            intergrade.append(dataset_name[idx])
            need_idx.append(idx)

    with open("./csv/nutrient_effect_pc_v2.1.csv", "r", encoding = "utf-8") as csv_file:    # csv file open    번호, 이름, 효능
        intergrade_dataset_name = []
        wb = csv.reader(csv_file)
        for line in wb:
            intergrade_dataset_name.append(line[1]) 
        for idx in need_idx:
            result.append(intergrade_dataset_name[idx])
        
    return result