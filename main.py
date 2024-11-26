from data_processing import load_and_process_data, preprocess_text
from recommendation import recommend_places
from sklearn.feature_extraction.text import TfidfVectorizer
import streamlit as st
from weather import get_weather  # Thêm import này để sử dụng hàm get_weather

# Đọc và xử lý dữ liệu
file_path = "data\DataSet.xlsx"
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
        recommendations = recommend_places(user_input, df, tfidf, preprocess_text)
        if recommendations.empty:
            st.write("Không tìm thấy địa điểm phù hợp với yêu cầu của bạn.")
        else:
            for _, row in recommendations.iterrows():
                st.subheader(row['Tên địa điểm'])
                st.write(f"**Mô tả:** {row['Mô tả']}")
                
                # Thêm thông tin thời tiết vào phần expander
                with st.expander("Chi tiết"):
                    st.write(f"**Địa chỉ:** {row['Vị trí']}")
                    # Lấy thông tin thời tiết cho địa điểm
                    weather_info = get_weather(row['Vị trí'])
                    
                    if weather_info:
                        st.write(f"**Nhiệt độ:** {weather_info['temperature']}°C")
                        st.write(f"**Thời tiết:** {weather_info['description']}")
                        st.write(f"**Độ ẩm:** {weather_info['humidity']}%")
                        if weather_info['icon']:
                            st.image(weather_info['icon'], width=50)
                    else:
                        st.write("Không thể lấy thông tin thời tiết cho địa điểm này.")
