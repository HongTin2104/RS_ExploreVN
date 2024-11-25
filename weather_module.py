import requests
from googletrans import Translator
from unidecode import unidecode

def get_weather(city):
    # Loại bỏ dấu tiếng Việt để tên thành phố chính xác hơn
    city_no_diacritics = unidecode(city)
    
    BASE_URL = "https://api.openweathermap.org/data/2.5/weather?"
    # Đọc API key từ file
    API_KEY = open('api_key', 'r').read().strip()
    
    # Hàm để lấy dữ liệu thời tiết
    def fetch_weather(city):
        url = BASE_URL + f"appid={API_KEY}&q={city}&units=metric"
        response = requests.get(url)
        
        if response.status_code == 200:
            return response.json()
        return None

    # Thử lấy thông tin thời tiết cho thành phố không dấu
    data = fetch_weather(city_no_diacritics)
    
    if data is None:
        # Nếu không tìm thấy, thử thêm "Tinh " vào tên thành phố và thử lại
        city_with_prefix = "Tinh " + city_no_diacritics
        data = fetch_weather(city_with_prefix)
    
    # Nếu lấy được dữ liệu
    if data:
        main = data.get('main', {})
        weather = data.get('weather', [{}])[0]
        temperature = main.get('temp', 0)
        celsius, fahrenheit = kelvin_to_celsius_fahrenheit(temperature)
        description = weather.get('description', 'Unknown weather')

        # Khởi tạo đối tượng dịch
        translator = Translator()
        description_vn = translator.translate(description, src='en', dest='vi').text
        
        icon = weather.get('icon', None)
        
        return {
            "temperature": round(celsius, 2),
            "description": description_vn,
            "humidity": main.get('humidity', 0),
            "icon": f"http://openweathermap.org/img/wn/{icon}@2x.png" if icon else None
        }
    
    return None

# Chuyển đổi nhiệt độ từ Kelvin sang Celsius và Fahrenheit
def kelvin_to_celsius_fahrenheit(kelvin):
    celsius = kelvin - 273.15
    fahrenheit = celsius * (9/5) + 32
    return celsius, fahrenheit
