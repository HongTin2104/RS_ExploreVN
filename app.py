import streamlit as st
import pandas as pd
from underthesea import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from collections import Counter

# Đọc dữ liệu từ file Excel
file_path = "data.xlsx"
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

# Tạo TF-IDF matrix từ mô tả đã xử lý
tfidf = TfidfVectorizer()
tfidf_matrix = tfidf.fit_transform(df['Mô tả sau tách'])

# Tính độ tương tự cosine
place_similarity = cosine_similarity(tfidf_matrix, tfidf_matrix)

# Hàm gợi ý địa điểm dựa trên từ khóa người dùng
def recommend_places(input_keywords, df, tfidf, num_recommendations=3):
    # Kết hợp các từ khóa của người dùng thành một chuỗi
    input_text = preprocess_text(" ".join(input_keywords))
    input_vector = tfidf.transform([input_text])
    
    # Tính độ tương tự cosine giữa từ khóa nhập và các mô tả địa điểm
    cosine_sim = cosine_similarity(input_vector, tfidf_matrix).flatten()
    
    # Lấy các chỉ số địa điểm có độ tương đồng cao nhất
    similar_indices = cosine_sim.argsort()[-num_recommendations:][::-1]
    
    # Lấy ra các địa điểm gợi ý
    recommendations = df.iloc[similar_indices]
    return recommendations

# Giao diện Streamlit
st.set_page_config(page_title="Vietnam Travel Recommendation System", layout="wide")

st.markdown("<h1 style='text-align: center; color: white;'>Vietnam Travel Recommendation System</h1>", unsafe_allow_html=True)

st.write("Nhập ba từ khóa để tìm kiếm các địa điểm du lịch tại Việt Nam phù hợp nhất.")

# Các input từ người dùng
keyword1 = st.text_input("Keyword 1", placeholder="Enter first keyword (e.g., beach)")
keyword2 = st.text_input("Keyword 2", placeholder="Enter second keyword (e.g., mountain)")
keyword3 = st.text_input("Keyword 3", placeholder="Enter third keyword (e.g., culture)")

if st.button("Submit"):
    if not (keyword1 and keyword2 and keyword3):
        st.write("Vui lòng nhập đủ 3 từ khóa.")
    else:
        # Nhập ba từ khóa từ người dùng
        user_keywords = [keyword1, keyword2, keyword3]
        
        # Gọi hàm để gợi ý các địa điểm
        recommendations = recommend_places(user_keywords, df, tfidf, num_recommendations=3)

        # Hiển thị các địa điểm gợi ý
        st.write("### Các địa điểm gợi ý phù hợp:")
        for _, row in recommendations.iterrows():
            st.write(f"- **{row['Tên địa điểm']}** (Vị trí: {row.get('Vị trí', 'Không rõ')})")
            st.write(f"  - Mô tả: {row['Mô tả']}")
