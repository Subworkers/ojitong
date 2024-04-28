# 프롬프트 엔지니어링

**`Knowledge Generation`**

- 네이버 뉴스 크롤링 최신순 -> 연관성 높은 기사 필터링 -> 프롬프트에 넘김  
    

**`Knowledge Selection`**  

- knowledge 선별 ( 프롬프트 엔지니어링 선정 ***REMOVED***


**`Knowledge Injection`**

어떤 데이터를 넣고 어떻게 프롬프팅할지

- Retrieval
- Template 
- Chaining

---
### 의존성

이 프로젝트를 실행하기 위해 다음과 같은 의존성이 필요합니다:

- `black==22.10.0`
- `fastapi==0.87.0`
- `mypy-extensions==0.4.3`
- `pydantic==1.10.2`
- `requests==2.28.1`
- `urllib3==1.26.12`
- `uvicorn==0.19.0`
- `python-dotenv==0.21.0`
- `pandas==1.5.2`
- `cryptography==39.0.2`
---
### workflow 
| 파일        | 역할                                                                                           |
|------------|------------------------------------------------------------------------------------------------|
| main.py    | 프로그램의 주 진입점으로, 각 운영사의 공지사항을 가져오는 함수들을 호출하고, 역 정보 변동을 확인하는 함수를 호출 |
| utils.py   | 공지사항을 가져오고 Slack에 전송하는 함수들이 정의된 파일                                      |

