import streamlit as st
import pandas as pd
from data_processing import load_and_process_data, preprocess_text
from recommendation import recommend_places
from sklearn.feature_extraction.text import TfidfVectorizer
from weather import get_weather
from translation import translate_to_vietnamese 

# Đọc và xử lý dữ liệu
file_path = "data/DataSet.xlsx"
df = load_and_process_data(file_path)

# Tạo TF-IDF cho mô tả của các địa điểm
tfidf = TfidfVectorizer()
tfidf.fit(df['Mô tả sau tách'])

# Giao diện Streamlit
st.title("Vietnam Travel Recommendation System")
user_input = st.text_area("Nhập mô tả mong muốn của bạn:")

if st.button("Tìm kiếm"):
    if not user_input.strip():
        st.error("Vui lòng nhập mô tả mong muốn.")
    else:
        # Kiểm tra xem ngôn ngữ của văn bản là tiếng Anh hay không
        if user_input.isascii():  # Nếu là tiếng Anh (ASCII characters)
            st.info("Phát hiện ngôn ngữ là tiếng Anh. Đang dịch sang tiếng Việt...")
            user_input = translate_to_vietnamese(user_input)  # Dịch sang tiếng Việt
            st.write(f"Mô tả: {user_input}")

        # Lấy danh sách địa điểm đề xuất
        recommendations = recommend_places(user_input, df, tfidf, preprocess_text)
        
        if recommendations.empty:
            st.write("Không tìm thấy địa điểm phù hợp với yêu cầu của bạn.")
        else:
            for _, row in recommendations.iterrows():
                st.subheader(row['Tên địa điểm'])
                st.write(f"**Mô tả:** {row['Mô tả']}")
                
                # Thêm thông tin thời tiết và hình ảnh vào phần expander với 2 cột
                with st.expander("Chi tiết"):
                    # Sử dụng st.columns để tạo 2 cột
                    col1, col2 = st.columns([3, 2])
                    
                    # Cột 1: Thông tin thời tiết
                    with col1:
                        st.write(f"**Địa chỉ:** {row['Vị trí']}")

                        # Lấy thông tin thời tiết cho địa điểm
                        weather_info = get_weather(row['Vị trí'])

                        if weather_info:
                            st.write(f"**Nhiệt độ:** {weather_info['temperature']}°C")
                            st.write(f"**Thời tiết:** {weather_info['description']}")
                            st.write(f"**Độ ẩm:** {weather_info['humidity']}%")
                            st.image(weather_info['icon'], width=80)
                        else:
                            st.write("Không thể lấy thông tin thời tiết cho địa điểm này.")
                    
                    # Cột 2: Hình ảnh địa điểm
                    with col2:
                        if pd.notnull(row['Ảnh']):
                            st.image(row['Ảnh'], caption=f"Hình ảnh {row['Tên địa điểm']}", use_container_width=True)
                        else:
                            st.write("Không có hình ảnh cho địa điểm này.")
