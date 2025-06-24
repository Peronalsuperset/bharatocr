from paddleocr import PaddleOCR
import logging

# Reduce paddleocr logging noise
logging.getLogger('ppocr').setLevel(logging.ERROR)

class OcrEngineManager:
    def __init__(self, supported_languages=None):
        # List of supported languages (add more as needed)
        if supported_languages is None:
            supported_languages = ['en', 'hi']
        self.supported_languages = supported_languages
        self.engines = {}

    def get_engine(self, lang):
        # Fallback to English if unsupported
        if lang not in self.supported_languages:
            lang = 'en'
        if lang not in self.engines:
            print(f"Initializing PaddleOCR for language: {lang}")
            self.engines[lang] = PaddleOCR(use_angle_cls=True, lang=lang, use_gpu=False)
        return self.engines[lang]

    def extract_text_from_image(self, image, lang='en'):
        engine = self.get_engine(lang)
        result = engine.ocr(image, cls=True)
        return result[0] if result and result[0] else []

ocr_engine_manager = OcrEngineManager() 