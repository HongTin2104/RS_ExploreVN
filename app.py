import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity



df = pd.DataFrame()

# Cấu hình Streamlit
st.set_page_config(page_title="Vietnam Travel Recommendation System", layout="wide")

st.markdown("<h1 style='text-align: center; color: white;'>Vietnam Travel Recommendation System</h1>", unsafe_allow_html=True)

# Nhập từ khóa từ người dùng
st.write("Nhập ba từ khóa để tìm kiếm các địa điểm du lịch tại Việt Nam phù hợp nhất.")

# Các input cho từ khóa
keyword1 = st.text_input("Keyword 1", placeholder="Enter first keyword (e.g., beach)")
keyword2 = st.text_input("Keyword 2", placeholder="Enter second keyword (e.g., mountain)")
keyword3 = st.text_input("Keyword 3", placeholder="Enter third keyword (e.g., culture)")

# Nút Submit để xử lý
if st.button("Submit"):
    if not (keyword1 and keyword2 and keyword3):
        st.write("Vui lòng nhập đủ 3 từ khóa.")
    else:
        # Tạo danh sách các từ khóa nhập vào
        user_keywords = [keyword1, keyword2, keyword3]
        user_input = " ".join(user_keywords)

        # Tính độ tương đồng giữa từ khóa nhập vào và các từ khóa của các địa điểm trong dataset
        vectorizer = TfidfVectorizer(stop_words='english')
        tfidf_matrix = vectorizer.fit_transform(pd.concat([df['Từ khóa'], pd.Series([user_input])], ignore_index=True))

        # Tính cosine similarity giữa các địa điểm và từ khóa người dùng nhập
        cosine_sim = cosine_similarity(tfidf_matrix[-1], tfidf_matrix[:-1]).flatten()

        # Lấy 3 địa điểm có độ tương đồng cao nhất
        similar_indices = cosine_sim.argsort()[-3:][::-1]

        st.write("### Các địa điểm gợi ý phù hợp:")
        for idx in similar_indices:
            st.write(f"- **{df['Tên địa điểm'][idx]}** (Vị trí: {df['Vị trí'][idx]})")
            st.write(f"  - Từ khóa: {df['Từ khóa'][idx]}")
