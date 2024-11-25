from underthesea import word_tokenize
from collections import Counter

# Hàm để tiền xử lý mô tả (bao gồm tách từ và loại bỏ stopwords)
def preprocess_text(text, vietnamese_stopwords):
    tokens = word_tokenize(text, format="text").split()
    tokens = [word for word in tokens if word.lower() not in vietnamese_stopwords]
    return ' '.join(tokens)

# Hàm để tạo danh sách stopwords từ DataFrame (dựa trên tần suất từ xuất hiện)
def create_stopwords(df):
    all_words = []
    for description in df['Mô tả']:
        words = word_tokenize(str(description), format='text').split()
        all_words.extend(words)

    word_freq = Counter(all_words)
    vietnamese_stopwords = [word for word, freq in word_freq.items() if freq > 10]
    
    return vietnamese_stopwords
