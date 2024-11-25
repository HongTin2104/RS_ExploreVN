import streamlit as st
import pandas as pd
from underthesea import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from collections import Counter
import datetime as dt
import requests
from googletrans import Translator

# Đọc dữ liệu từ file Excel
file_path = "DataSet.xlsx"
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

import requests
from googletrans import Translator
from unidecode import unidecode  # Import thư viện unidecode

def get_weather(city):
    # Chuyển tên thành phố về tiếng Việt không dấu
    city_no_diacritics = unidecode(city)
    
    BASE_URL = "https://api.openweathermap.org/data/2.5/weather?"
    API_KEY = open('api_key', 'r').read().strip()
    
    # Hàm để lấy dữ liệu thời tiết
    def fetch_weather(city):
        url = BASE_URL + f"appid={API_KEY}&q={city}"
        response = requests.get(url)
        
        if response.status_code == 200:
            return response.json()
        return None

    # Thử lấy thông tin thời tiết cho thành phố đầu tiên (tiếng Việt không dấu)
    data = fetch_weather(city_no_diacritics)
    
    if data is None:
        # Nếu không tìm thấy, thử lại với tiền tố "Tinh " cho thành phố
        city_with_prefix = "Tinh " + city_no_diacritics
        data = fetch_weather(city_with_prefix)
    
    # Khởi tạo đối tượng dịch
    translator = Translator()
    
    if data:
        main = data.get('main', {})
        weather = data.get('weather', [{}])[0]
        temperature = main.get('temp', 0)
        celsius, _ = kelvin_to_celsius_fahrenheit(temperature)
        description = weather.get('description', 'Unknown weather')

        # Dịch mô tả thời tiết
        description_vn = translator.translate(description, src='en', dest='vi').text
        icon = weather.get('icon', None)
        
        return {
            "temperature": round(celsius, 2),
            "description": description_vn,
            "humidity": main.get('humidity', 0),
            "icon": f"http://openweathermap.org/img/wn/{icon}@2x.png" if icon else None
        }
    
    return None

def kelvin_to_celsius_fahrenheit(kelvin):
    celsius = kelvin - 273.15
    fahrenheit = celsius * (9/5) + 32
    return celsius, fahrenheit

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
            # Tạo 3 cột cho mỗi địa điểm
            col1, col2, col3 = st.columns([4, 4, 4])  # Cột 1 và cột 2 chia đều không gian, cột 3 để trống

            # Dòng 1: Tên địa điểm
            with col1:
                st.markdown(f"**{row['Tên địa điểm']}** (Vị trí: {row.get('Vị trí', 'Không rõ')})")

            # Dòng 2: Mô tả
            with col1:
                st.write(f"**Mô tả:** {row['Mô tả']}")

            # Dòng 3: Hình ảnh địa điểm và thông tin thời tiết
            with col1:
                if pd.notna(row['Ảnh']):
                    st.image(row['Ảnh'], caption=row['Tên địa điểm'], width=350)  # Hiển thị ảnh
                else:
                    st.write("Không có ảnh")

            with col2:
                if pd.notna(row['Vị trí']):
                    weather = get_weather(row['Vị trí'])
                    if weather:
                        st.write(f"**Thời tiết tại {row['Vị trí']}:**")
                        col1, col2 = st.columns([1, 5])
                        with col1:
                            if weather["icon"]:
                                st.image(weather["icon"], width=50)  # Hiển thị icon thời tiết
                        with col2:
                            st.write(f"- Nhiệt độ: {weather['temperature']}°C")
                            st.write(f"- Mô tả: {weather['description']}")
                            st.write(f"- Độ ẩm: {weather['humidity']}%")
                    else:
                        st.write(f"Không thể lấy thông tin thời tiết cho {row['Vị trí']}.")
                else:
                    st.write("Không có thông tin thời tiết.")
