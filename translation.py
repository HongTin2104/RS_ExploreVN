# translation.py
from googletrans import Translator

# Hàm dịch văn bản từ tiếng Anh sang tiếng Việt
def translate_to_vietnamese(text):
    try:
        translator = Translator()
        result = translator.translate(text, src='en', dest='vi')  # Dịch từ tiếng Anh sang tiếng Việt
        return result.text
    except Exception as e:
        return f"Lỗi dịch văn bản: {e}"
