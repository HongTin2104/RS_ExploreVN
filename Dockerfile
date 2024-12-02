# Bắt đầu từ Ubuntu 22.04
FROM ubuntu:22.04

# Cập nhật hệ thống và cài đặt các gói cơ bản
RUN apt update && apt upgrade -y && apt install -y \
    wget \
    build-essential \
    libssl-dev \
    zlib1g-dev \
    libncurses5-dev \
    libnss3-dev \
    libsqlite3-dev \
    libreadline-dev \
    libffi-dev \
    libbz2-dev \
    python3.10 \
    python3.10-venv \
    python3.10-dev \
    curl \
    git \
    && apt clean

# Cài đặt pip cho Python 3.10
RUN curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py \
    && python3.10 get-pip.py \
    && rm get-pip.py

# Cài đặt các thư viện yêu cầu bao gồm openpyxl
RUN python3.10 -m pip install --no-cache-dir \
    streamlit \
    pandas \
    scikit-learn \
    underthesea \
    googletrans==4.0.0-rc1 \
    requests \
    unidecode \
    openpyxl  # Cài đặt openpyxl để Pandas có thể đọc tệp Excel

# Tạo thư mục data trong container
RUN mkdir -p /app/data

# Sao chép các file Python và tệp dữ liệu vào container
COPY data_processing.py /app/
COPY api_key/ /app/
COPY main.py /app/
COPY weather.py /app/
COPY recommendation.py /app/
COPY translation.py /app/
COPY data/DataSet.xlsx /app/data/

# Cài đặt môi trường làm việc (nếu cần thiết)
WORKDIR /app

# Mở cổng cho Streamlit (nếu bạn muốn chạy Streamlit)
EXPOSE 8501

# Lệnh mặc định khi chạy container (để chạy Streamlit app)
CMD ["streamlit", "run", "main.py", "--server.enableCORS=false", "--server.port=8501"]

# docker build -t vietnam-travel-recommendation-system .
# docker run -it -p 8501:8501 --name vietnam-travel-recommendation-system vietnam-travel-recommendation-system
# docker run vietnam-travel-recommendation-system