# OSS-Project-AI: 영양제 추천 AI 시스템

## 프로젝트 개요

이 프로젝트는 사용자의 건강 상태나 증상을 분석하여 적절한 영양제를 추천하는 AI 시스템입니다. 자연어 처리와 머신러닝을 활용하여 개인화된 영양제 추천 서비스를 제공합니다.

## 주요 기능

### 1. AI 기반 영양제 추천
- **의사 역할 AI**: 사용자의 건강 관련 질문에 대해 의사처럼 답변
- **개인화 추천**: 증상과 상태에 맞는 맞춤형 영양제 추천
- **다국어 지원**: 한국어-영어 번역을 통한 글로벌 서비스

### 2. 자연어 처리
- **BERT 모델 활용**: `jhgan/ko-sroberta-multitask` 모델을 사용한 의미 분석
- **FAISS 벡터 검색**: 고속 유사도 검색을 통한 정확한 영양제 매칭
- **텍스트 전처리**: KoNLPy와 PyKoSpacing을 활용한 한국어 텍스트 처리

### 3. 데이터 분석
- **영양제 데이터베이스**: 600여 종의 영양제 정보와 효능 데이터
- **인기도 분석**: Google 검색량 기반 영양제 인기도 측정
- **효능 분석**: 영양제별 상세 효능 정보 제공

## 📁 프로젝트 구조

```
OSS-Project-AI/
├── AI/                          # AI 모델 및 핵심 로직
│   ├── app.py                   # Flask 웹 서버
│   ├── chat.py                  # GPT 기반 챗봇
│   ├── test.py                  # FAISS 벡터 검색
│   ├── nutrientAwareness.py     # 영양제 인기도 분석
│   ├── excelDataCutting.py      # 엑셀 데이터 전처리
│   ├── papago.py                # 번역 API
│   └── ...
├── csv/                         # 영양제 데이터
│   ├── nutrient_effect_pc_v2.1.csv
│   ├── nutrient_effect_pc_v2.2.csv
│   └── nutrient_effect_pc_v2.3.csv
├── documents/                   # 문서 및 결과 파일
│   ├── 영양제.txt
│   ├── result.xlsx
│   └── ...
├── excel/                       # 엑셀 데이터
│   └── ossexcel2.xlsx
└── README.md
```

## 🛠️ 기술 스택

### Backend
- **Python 3.x**
- **Flask**: 웹 서버 프레임워크
- **OpenAI GPT-3.5-turbo**: 챗봇 AI
- **Sentence Transformers**: 텍스트 임베딩
- **FAISS**: 벡터 검색 엔진

### Data Processing
- **Pandas**: 데이터 분석 및 처리
- **NumPy**: 수치 계산
- **KoNLPy**: 한국어 자연어 처리
- **PyKoSpacing**: 한국어 띄어쓰기 교정

### APIs
- **Naver Papago API**: 한국어-영어 번역
- **OpenAI API**: GPT 모델 사용

## 설치 및 실행

### 1. 환경 설정
```bash
# 저장소 클론
git clone [repository-url]
cd OSS-Project-AI

# Python 가상환경 생성 (권장)
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 필요한 패키지 설치
pip install -r requirements.txt
```

### 2. API 키 설정
```python
# AI/chat.py에서 OpenAI API 키 설정
API_KEY = "your-openai-api-key"

# AI/papago.py에서 Naver Papago API 키 설정
api_key_list = [
    ["your-client-id", "your-client-secret"]
]
```

### 3. 서버 실행
```bash
cd AI
python app.py
```

서버가 `http://localhost:5000`에서 실행됩니다.

## API 엔드포인트

### 1. 영양제 검색
```
GET /ask/{user_input}
```
사용자 입력에 따른 영양제 추천

### 2. AI 챗봇
```
GET /chat/{user_chat}
```
GPT 기반 건강 상담 및 영양제 추천

## 💡 사용 예시

### 영양제 검색
```bash
curl "http://localhost:5000/ask/피로감"
```

**입력 예시:**
- "피로감"
- "면역력 향상"
- "소화 개선"
- "관절 건강"
- "피부 미용"

**결과 예시:**
```json
[
  "비타민B",
  "코엔자임Q10", 
  "마그네슘",
  "오메가3",
  "프로바이오틱"
]
```

### AI 상담
```bash
curl "http://localhost:5000/chat/요즘 피로하고 집중력이 떨어져요"
```

**입력 예시:**
- "요즘 피로하고 집중력이 떨어져요"
- "면역력이 약해진 것 같아요"
- "소화가 안 되고 속이 더부룩해요"
- "관절이 아프고 뻣뻣해요"
- "피부가 건조하고 탄력이 없어졌어요"

**결과 예시:**
```
안녕하세요. 피로감과 집중력 저하 증상에 대해 말씀해 주셨네요.

이러한 증상들은 여러 가지 원인이 있을 수 있습니다:
1. 수면 부족이나 스트레스
2. 영양소 부족 (특히 비타민B군, 마그네슘)
3. 철분 결핍
4. 갑상선 기능 저하

개선을 위한 권장사항:
- 충분한 수면 (7-8시간)
- 규칙적인 운동
- 균형 잡힌 식단
- 스트레스 관리

추천 영양제
비타민B복합체
코엔자임Q10
마그네슘
오메가3
철분제

- [구매 링크]
- [구매 링크]
- [구매 링크]
- [구매 링크]
- [구매 링크]
```

### 상세한 API 응답 구조

**영양제 검색 API (`/ask/{query}`)**
- **입력**: 검색하고 싶은 증상이나 효능 키워드
- **출력**: 관련된 영양제 5개 리스트
- **처리 방식**: FAISS 벡터 검색을 통한 유사도 기반 추천

**AI 상담 API (`/chat/{message}`)**
- **입력**: 건강 관련 질문이나 증상 설명
- **출력**: 의사 역할 AI의 상담 답변 + 추천 영양제
- **처리 방식**: GPT-3.5-turbo + 번역 API + 영양제 매칭

## 데이터베이스

### 영양제 정보
- **총 600여 종**의 영양제 데이터
- **효능별 분류**: 면역력, 소화, 피부, 관절 등
- **상세 정보**: 성분, 효능, 복용법, 주의사항

### 데이터 구조
```csv
번호,영양제명,효능설명
0,프리바이오틱,프리바이오틱스 체내 효소 분해...
1,글루코아밀라아제,글루코아밀라아제는 α-14 결합...
```

## 개발 환경 설정

### 필수 패키지
- requirements.txt 제공
```
flask
openai
sentence-transformers
faiss-cpu
pandas
numpy
konlpy
pykospacing
openpyxl
requests
beautifulsoup4
matplotlib
scikit-learn
```
