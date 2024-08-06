
import io
from PIL import Image, ImageDraw, ImageFont
from data.processors.s3_image_uploader import S3ImageUploader

class CardNewsCreator:
    def __init__(self, image_path, font_path, s3_path***REMOVED***:
        self.image_path = image_path
        self.font_path = font_path
        self.image = self._load_image(image_path***REMOVED***
        self.draw = ImageDraw.Draw(self.image***REMOVED***
        self.s3_path = s3_path
        self.s3_image_uploader = S3ImageUploader(***REMOVED***

    def _load_image(self, path***REMOVED***:
        # 배경 이미지 로드
        return Image.open(path***REMOVED***

    # main function
    def create_card_news(self, keyword_info, category***REMOVED***:
        title_font = self._get_font(500***REMOVED***
        tail_font = self._get_font(100***REMOVED***
        content_font = self._get_content_font(keyword_info***REMOVED***
        
        width, height= self.image.size
        title_text = self._get_title_text(category***REMOVED***
        self._draw_text_centered(title_text, width / 2, height * 0.2, title_font, fill="White"***REMOVED***
        self._draw_text_centered(keyword_info['date'***REMOVED***, width / 2, height * 0.55, content_font, fill="Red"***REMOVED***
        self._draw_text_centered(keyword_info['line'***REMOVED***, width / 2, height * 0.75, content_font, fill="Red"***REMOVED***
        self._draw_text_centered('오늘의 지하철 소식통', width / 2, height * 0.925, tail_font, fill="White"***REMOVED***
        
        self._save_image(***REMOVED***

    def _get_font(self, size***REMOVED***:
        # 폰트 설정
        return ImageFont.truetype(self.font_path, size***REMOVED***

    def _draw_text_centered(self, text, x, y, font, fill="White"***REMOVED***:
        # 텍스트 박스 크기 측정
        text_width, text_height = self.draw.textbbox((0, 0***REMOVED***, text, font=font***REMOVED***[2:***REMOVED***
        # 텍스트 그리기, x 위치를 중앙 조정
        self.draw.text((x - text_width / 2, y - text_height / 2***REMOVED***, text, font=font, fill=fill***REMOVED***

    def _get_content_font(self, info***REMOVED***:
        # content_font 크기 동적 설정
        content_text_length = max(len(info['date'***REMOVED******REMOVED***, len(info['line'***REMOVED******REMOVED******REMOVED***
        if content_text_length >= 23:
            return self._get_font(150***REMOVED***
        elif 19 <= content_text_length < 23:
            return self._get_font(180***REMOVED***
        elif 10 <= content_text_length < 19:
            return self._get_font(200***REMOVED***
        else:
            return self._get_font(400***REMOVED***

    def _get_title_text(self, category***REMOVED***:
        categories = {"지연": "지하철 지연", "파업": "지하철 파업", "timetable": "시간표 변경", "사고": "지하철 사고", "연착": "지하철 연착","연장":"지하철 연장"***REMOVED***
        return categories.get(category, "정보"***REMOVED***

    def _save_image(self***REMOVED***:
        TEMP = io.BytesIO(***REMOVED***
        self.image.save(TEMP, format="PNG"***REMOVED***
        TEMP.seek(0***REMOVED***
    
        self.s3_image_uploader.upload_image(TEMP, self.s3_path***REMOVED***