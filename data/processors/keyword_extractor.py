# 카드뉴스 키워드 추출

import re

class KeywordExtractor:
    def extract_info(self, content, category):
        clean_content = self._clean_text(content)
        patterns = self._get_patterns(category)
        return {
            "date": self._extract_keywords_by_pattern(clean_content, patterns['date']),
            "line": self._extract_keywords_by_pattern(clean_content, patterns['line'])
        }

    def _clean_text(self, text):
        text = re.sub(r'\*\*', '', text)
        text = re.sub(r'\{\{|\}\}', '', text)
        text = re.sub(r': ', '', text)
        text = re.sub(r'- ', '', text)
        return text

    def _get_patterns(self, category):
        base_patterns = {
            "date": "일시",
            "line": "노선"
        }
        category_patterns = {
            "지연": "지연/사고",
            "사고": "지연/사고",
            "연착": "지연/사고",
            "파업": "파업",
            "연장": "연장",
            "변경": "변경"
        }

        return {
            key: [
                rf"{category_patterns.get(category, '변경')} {suffix}\s*\n\s*(.+?)(?=\n\n|\n\s*{{|\n\s*\*\*|$)",
                rf"{category_patterns.get(category, '변경')} {suffix}\s*\n\s*(.+?)(?:\r?\n|$)",
                rf"{category_patterns.get(category, '변경')} {suffix}\s*(.+?)(?:\r?\n|$)"
            ] for key, suffix in base_patterns.items()
        }

    def _extract_keywords_by_pattern(self, content, patterns):
        for pattern in patterns:
            match = re.search(pattern, content, re.DOTALL)
            if match:
                return ', '.join([data.strip() for data in match.group(1).split('\n')])
        return "정보 없음"
