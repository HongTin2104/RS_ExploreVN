import pandas as pd
from underthesea import word_tokenize
from collections import Counter

# Đọc dữ liệu từ file Excel
def load_data(file_path):
    df = pd.read_excel(file_path)
    # Tách từ và đếm tần suất
    all_words = []
    for description in df['Mô tả']:
        words = word_tokenize(str(description), format='text').split()
        all_words.extend(words)

    # Tạo danh sách stop words
    word_freq = Counter(all_words)
    vietnamese_stopwords = [word for word, freq in word_freq.items() if freq > 10]

    # Hàm tiền xử lý mô tả
    def preprocess_text(text):
        tokens = word_tokenize(text, format="text").split()
        tokens = [word for word in tokens if word.lower() not in vietnamese_stopwords]
        return ' '.join(tokens)

    # Áp dụng tiền xử lý
    df['Mô tả sau tách'] = df['Mô tả'].apply(preprocess_text)
    return df
