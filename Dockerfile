FROM python:3.9.20

# Thiết lập thư mục làm việc trong container
WORKDIR /app

# Copy toàn bộ project vào container
COPY . .

RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y

# Cập nhật pip và cài đặt các thư viện cần thiết
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Mở cổng API (giả sử chạy trên cổng 8000)
EXPOSE 8000

# Chạy API (thay đổi nếu cần)
CMD ["python", "app.py"]