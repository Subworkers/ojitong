
import io
from PIL import Image, ImageDraw, ImageFont


class CardNewsCreator:
    def __init__(self, image_path, font_path, s3_path):
        self.image_path = image_path
        self.font_path = font_path
        self.image = self._load_image(image_path)
        self.draw = ImageDraw.Draw(self.image)
        self.s3_path = s3_path

    def _load_image(self, path):
        # 배경 이미지 로드
        return Image.open(path)

    # main function
    def create_card_news(self, keyword_info, category):
        title_font = self._get_font(500)
        tail_font = self._get_font(100)
        content_font = self._get_content_font(keyword_info)
        
        width, height= self.image.size
        title_text = self._get_title_text(category)
        self._draw_text_centered(title_text, width / 2, height * 0.2, title_font, fill="White")
        self._draw_text_centered(keyword_info['date'], width / 2, height * 0.55, content_font, fill="Red")
        self._draw_text_centered(keyword_info['line'], width / 2, height * 0.75, content_font, fill="Red")
        self._draw_text_centered('오늘의 지하철 소식통', width / 2, height * 0.925, tail_font, fill="White")
        
        self._save_image()

    def _get_font(self, size):
        # 폰트 설정
        return ImageFont.truetype(self.font_path, size)

    def _draw_text_centered(self, text, x, y, font, fill="White"):
        # 텍스트 박스 크기 측정
        text_width, text_height = self.draw.textbbox((0, 0), text, font=font)[2:]
        # 텍스트 그리기, x 위치를 중앙 조정
        self.draw.text((x - text_width / 2, y - text_height / 2), text, font=font, fill=fill)

    def _get_content_font(self, info):
        # content_font 크기 동적 설정
        content_text_length = max(len(info['date']), len(info['line']))
        if content_text_length >= 23:
            return self._get_font(150)
        elif 19 <= content_text_length < 23:
            return self._get_font(180)
        elif 10 <= content_text_length < 19:
            return self._get_font(200)
        else:
            return self._get_font(400)

    def _get_title_text(self, category):
        categories = {"지연": "지하철 지연", "파업": "지하철 파업", "timetable": "시간표 변경", "사고": "지하철 사고", "연착": "지하철 연착","연장":"지하철 연장"}
        return categories.get(category, "정보")

    def _save_image(self):
        TEMP = io.BytesIO()
        self.image.save(TEMP, format="PNG")
        TEMP.seek(0)
    
        self.s3_image_uploader.upload_image(TEMP, self.s3_path)