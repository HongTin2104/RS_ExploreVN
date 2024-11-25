from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd

# Tạo TF-IDF matrix từ mô tả đã xử lý
def create_tfidf_matrix(df):
    tfidf = TfidfVectorizer()
    tfidf_matrix = tfidf.fit_transform(df['Mô tả sau tách'])
    return tfidf, tfidf_matrix

# Hàm gợi ý địa điểm dựa trên từ khóa người dùng
def recommend_places(input_keywords, df, tfidf, tfidf_matrix, num_recommendations=3):
    # Kết hợp các từ khóa của người dùng thành một chuỗi
    input_text = " ".join(input_keywords)
    input_vector = tfidf.transform([input_text])
    
    # Tính độ tương tự cosine giữa từ khóa nhập và các mô tả địa điểm
    cosine_sim = cosine_similarity(input_vector, tfidf_matrix).flatten()
    
    # Lấy các chỉ số địa điểm có độ tương đồng cao nhất
    similar_indices = cosine_sim.argsort()[-num_recommendations:][::-1]
    
    # Lấy ra các địa điểm gợi ý
    recommendations = df.iloc[similar_indices]
    return recommendations
