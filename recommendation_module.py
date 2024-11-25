import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from underthesea import word_tokenize

from preprocessing_module import preprocess_text

def recommend_places(input_keywords, df, tfidf, tfidf_matrix, num_recommendations=3):
    # Kết hợp các từ khóa của người dùng thành một chuỗi và tiền xử lý
    input_text = preprocess_text(" ".join(input_keywords))
    input_vector = tfidf.transform([input_text])
    
    # Tính độ tương tự cosine giữa từ khóa nhập và các mô tả địa điểm
    cosine_sim = cosine_similarity(input_vector, tfidf_matrix).flatten()
    
    # Lấy các chỉ số địa điểm có độ tương đồng cao nhất
    similar_indices = cosine_sim.argsort()[-num_recommendations:][::-1]
    
    # Lấy ra các địa điểm gợi ý
    recommendations = df.iloc[similar_indices]
    return recommendations
