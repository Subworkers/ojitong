# 카드뉴스 키워드 추출

import re

class KeywordExtractor:
    def extract_info(self, content, category***REMOVED***:
        clean_content = self._clean_text(content***REMOVED***
        patterns = self._get_patterns(category***REMOVED***
        return {
            "date": self._extract_keywords_by_pattern(clean_content, patterns['date'***REMOVED******REMOVED***,
            "line": self._extract_keywords_by_pattern(clean_content, patterns['line'***REMOVED******REMOVED***
        ***REMOVED***

    def _clean_text(self, text***REMOVED***:
        text = re.sub(r'\*\*', '', text***REMOVED***
        text = re.sub(r'\{\{|\***REMOVED***\***REMOVED***', '', text***REMOVED***
        text = re.sub(r': ', '', text***REMOVED***
        text = re.sub(r'- ', '', text***REMOVED***
        return text

    def _get_patterns(self, category***REMOVED***:
        base_patterns = {
            "date": "일시",
            "line": "노선"
        ***REMOVED***
        category_patterns = {
            "지연": "지연/사고",
            "사고": "지연/사고",
            "연착": "지연/사고",
            "파업": "파업",
            "연장": "연장",
            "변경": "변경"
        ***REMOVED***

        return {
            key: [
                rf"{category_patterns.get(category, '변경'***REMOVED******REMOVED*** {suffix***REMOVED***\s*\n\s*(.+?***REMOVED***(?=\n\n|\n\s*{{|\n\s*\*\*|$***REMOVED***",
                rf"{category_patterns.get(category, '변경'***REMOVED******REMOVED*** {suffix***REMOVED***\s*\n\s*(.+?***REMOVED***(?:\r?\n|$***REMOVED***",
                rf"{category_patterns.get(category, '변경'***REMOVED******REMOVED*** {suffix***REMOVED***\s*(.+?***REMOVED***(?:\r?\n|$***REMOVED***"
            ***REMOVED*** for key, suffix in base_patterns.items(***REMOVED***
        ***REMOVED***

    def _extract_keywords_by_pattern(self, content, patterns***REMOVED***:
        for pattern in patterns:
            match = re.search(pattern, content, re.DOTALL***REMOVED***
            if match:
                return ', '.join([data.strip(***REMOVED*** for data in match.group(1***REMOVED***.split('\n'***REMOVED******REMOVED******REMOVED***
        return "정보 없음"
