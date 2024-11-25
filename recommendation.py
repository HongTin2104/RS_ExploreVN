from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd

def recommend_places(user_input, df, tfidf, preprocess_text, num_recommendations=3):
    # Tiền xử lý văn bản đầu vào của người dùng
    input_text = preprocess_text(user_input)
    if not input_text:
        return pd.DataFrame()  # Nếu không có từ nào sau xử lý, trả về DataFrame rỗng

    # Chuyển đổi văn bản đầu vào thành vector
    input_vector = tfidf.transform([input_text])

    # Tính toán độ tương đồng cosine giữa văn bản đầu vào và các mô tả trong DataFrame
    tfidf_matrix = tfidf.transform(df['Mô tả sau tách'])
    cosine_sim = cosine_similarity(input_vector, tfidf_matrix).flatten()

    # Gợi ý những địa điểm có độ tương đồng cao nhất
    indices = cosine_sim.argsort()[-num_recommendations:][::-1]
    recommendations = df.iloc[indices].copy()
    recommendations['Độ tương đồng (%)'] = (cosine_sim[indices] * 100).round(2)
    return recommendations[['Tên địa điểm', 'Mô tả', 'Độ tương đồng (%)']]
