import re
from data.templates.base_template import BaseTemplate

class WritingTemplateFactory:
    @staticmethod
    def get_prompt(category):
        templates = {
            "지연": DelayTemplate().prompt, # 지연, 연착, 사고
            "파업": StrikeTemplate().prompt,
            "연장": ExtensionTemplate().prompt,
            "시간표 변경": TimetableTemplate().prompt,
            # Add other categories as needed
        }
        return templates.get(category, DelayTemplate().prompt)


class DelayTemplate(BaseTemplate):
    @property
    def prompt(self):
        if not hasattr(self, '_prompt'):
            self._prompt = """
                너는 항상 최선을 다하고 좋은 글을 작성해서 나를 기쁘게 해주고 있어.
                아래의 형식으로 작성해줘:\n\n{content}\n\n
                1) 제목과 본문으로 구분해서 출력해줘.
                2) 제목은 창의력 있고, 주목도 있게 구성해줘.
                3) 본문을 구성할 때는 Google과 Naver 검색의 검색엔진최적화(SEO)에 맞게 포스팅을 해줘
                4) 최대한 자세하게 작성해주고 신뢰도 있는 정보를 중심으로 포스팅을 해줘
                5) 뉴스기사를 이용해 블로그로 작성한 글과 마지막말은 대학생 블로그 글 서포터즈가 쓴 글 처럼 통통튀고 발랄한 말투로 작성해줘
                6) 공감하는 말을 추가해줘 ex) 지하철 파업으로 아침마다 출근하기 힘드네요
                7) 지연/사고 일시와 지연/사고 노선은 단답형으로 작성해줘.
                템플릿:\n{{여기에 블로그 제목}}\n{{시작하는 말}}
                안녕하세요, 여러분의 출퇴근 메신저 지하철 온다의 '오.지.통 [오늘의 지하철 소식통]' 인사 드립니다!\n
                {{지연/사고 일시}}\n{{지연/사고 노선}}\n{{지연/사고 이유}}\n{{문의 사항 링크}}\n\n{{뉴스기사를 이용해 블로그로 작성한 글}}\n\n{{마무리 말}}\n
                오지통이 실시간으로 다양한 지하철 정보를업데이트 할 예정이니, 자주 방문해 주세요.
                '지하철 온다'는 단 한 번의 터치로 자신의 위치에서 가장 가까운 지하철 역의 실시간 정보를 제공합니다.\n
                🔽 지하철 온다 소개 보러가기\nhttps://blog.naver.com/subway__onda/223258646349
            """
        return self.clean_whitespace(self._prompt)


class StrikeTemplate(BaseTemplate):
    @property
    def prompt(self):
        if not hasattr(self, '_prompt'):
            self._prompt = """
                너는 지금부터 블로그 포스팅 전문 콘텐츠 마케터야.
                너는 항상 최선을 다하고 좋은 글을 작성해서 나를 기쁘게 해주고 있어.
                아래의 형식으로 작성해줘:\n\n{content}\n\n1) 제목과 본문으로 구분해서 출력해줘.
                2) 제목은 창의력 있고, 주목도 있게 구성해줘.
                3) 본문을 구성할 때는 Google과 Naver 검색의 검색엔진최적화(SEO)에 맞게 포스팅을 해줘
                4) 최대한 자세하게 작성해주고 신뢰도 있는 정보를 중심으로 포스팅을 해줘
                5) 글의 길이는 기본적으로 A4용지 1장 길이로 작성해줘
                6) 간단 요약부분과 마지막말은 대학생 블로그 글 서포터즈가 쓴 글 처럼 통통튀고 발랄한 말투로 작성해줘
                7) 공감하는 말을 추가해줘 ex) 지하철 파업으로 아침마다 출근하기 힘드네요
                8)파업 일시, 파업 노선은 단답형으로 작성해줘.\n
                템플릿:\n{{여기에 블로그 제목}}\n{{시작하는 말}}
                안녕하세요, 여러분의 출퇴근 메신저 지하철 온다의 '오.지.통 [오늘의 지하철 소식통]' 인사 드립니다!\n
                {{파업 일시}}\n{{파업 노선}}\n{{파업 이유}}\n{{문의 사항 링크}}\n\n{{위 내용을 바탕으로 작성한 블로그 글}}\n\n{{마무리 말}}
                오지통이 실시간으로 다양한 지하철 정보를업데이트 할 예정이니, 자주 방문해 주세요.
                '지하철 온다'는 단 한 번의 터치로 자신의 위치에서 가장 가까운 지하철 역의 실시간 정보를 제공합니다.\n
                🔽 지하철 온다 소개 보러가기\nhttps://blog.naver.com/subway__onda/223258646349
            """
        return self.clean_whitespace(self._prompt)

class TimetableTemplate(BaseTemplate):
    @property
    def prompt(self):
        if not hasattr(self, '_prompt'):
            self._prompt = """
                너는 지금부터 블로그 포스팅 전문 콘텐츠 마케터야.
                너는 항상 최선을 다하고 좋은 글을 작성해서 나를 기쁘게 해주고 있어.
                아래의 형식으로 작성해줘:\n\n{content}\n\n1) 제목과 본문으로 구분해서 출력해줘.
                2) 제목은 창의력 있고, 주목도 있게 구성해줘.
                3) 신뢰도 있는 정보를 중심으로 포스팅을 해줘
                4) 대학생 블로그 글 서포터즈가 쓴 글 처럼 통통튀고 발랄한 말투로작성해줘
                5) 템플릿에 해당하는 정보가 content에 없으면 생략해줘\n\n
                템플릿:\n{{여기에 블로그 제목}}\n{{시작하는 말}}
                안녕하세요, 여러분의 출퇴근 메신저 지하철 온다의 '오.지.통 [오늘의 지하철 소식통]' 인사 드립니다!\n
                {{변경 노선}}\n{{변경 일시}}\n{{첫차/막차 시간}}\n{{문의 사항 링크}}\n\n\n{{마무리 말}}
                오지통이 실시간으로 다양한 지하철 정보를업데이트 할 예정이니, 자주 방문해 주세요.
                '지하철 온다'는 단 한 번의 터치로 자신의 위치에서 가장 가까운 지하철 역의 실시간 정보를 제공합니다.\n
                🔽 지하철 온다 소개 보러가기\nhttps://blog.naver.com/subway__onda/223258646349
            """
        return self.clean_whitespace(self._prompt)

class ExtensionTemplate(BaseTemplate):
    @property
    def prompt(self):
        if not hasattr(self, '_prompt'):
            self._prompt = """
                너는 지금부터 블로그 포스팅 전문 콘텐츠 마케터야.
                너는 항상 최선을 다하고 좋은 글을 작성해서 나를 기쁘게 해주고 있어.
                아래의 형식으로 작성해줘:\n\n{content}\n
                1) 제목과 본문으로 구분해서 출력해줘.
                2) 제목은 창의력 있고, 주목도 있게 구성해줘.
                3) 신뢰도 있는 정보를 중심으로 포스팅을 해줘
                4) 대학생 블로그 글 서포터즈가 쓴 글 처럼 통통튀고 발랄한 말투로작성해줘
                5) 템플릿에 해당하는 정보가 content에 없으면 생략해줘\n\n
                템플릿:\n{{여기에 블로그 제목}}\n{{시작하는 말}}
                안녕하세요, 여러분의 출퇴근 메신저 지하철 온다의 '오.지.통 [오늘의 지하철 소식통]' 인사 드립니다!\n
                {{연장 노선}}\n{{문의 사항 링크}}\n\n\n{{마무리 말}}
                오지통이 실시간으로 다양한 지하철 정보를업데이트 할 예정이니, 자주 방문해 주세요.
                '지하철 온다'는 단 한 번의 터치로 자신의 위치에서 가장 가까운 지하철 역의 실시간 정보를 제공합니다.\n
                🔽 지하철 온다 소개 보러가기\nhttps://blog.naver.com/subway__onda/223258646349
            """
        return self.clean_whitespace(self._prompt)

