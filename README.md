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
workflow 
| main.py | 파일은 프로그램의 주 진입점 | 여기서는 각 운영사의 공지사항을 가져오는 함수들을 호출, 역 정보 변동을 확인하는 함수를 호출 |
| utils.py | 파일에는 실제로 공지사항을 가져오고 Slack에 전송하는 함수들이 정의 |
