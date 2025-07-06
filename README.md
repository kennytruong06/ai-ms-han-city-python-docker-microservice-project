# Hancity AI Microservice (AI MS)

## 📌 Giới thiệu

Đây là mã nguồn microservice AI của Hancity, cung cấp API kiểm duyệt nội dung tự động cho hệ thống đăng bài. Dịch vụ này sử dụng các mô hình AI để phát hiện nội dung nhạy cảm (NSFW), bạo lực trong ảnh/video và kiểm tra từ ngữ phản cảm trong văn bản. API được thiết kế để tích hợp trực tiếp vào hệ thống backend, không có giao diện người dùng (UI), chỉ cung cấp các endpoint RESTful cho các dịch vụ khác gọi tới.


## 🚀 Features

- **Detect offensive words** in text inputs using a predefined list of negative words.
- **Analyze images** to determine NSFW content using NudeNet and ViT Base Violence Detection.
- **Analyze videos** by extracting frames and checking for NSFW content.
- **Support multiple file uploads:** PNG, JPG, JPEG, MP4, AVI, MOV, MKV.
- **REST API interface** for easy integration.
- **Secure file handling**, processing, and automatic deletion after analysis.

## 🛠 Installation (How to run by docker)

### Create the folder 

```sh
uploaded
```
uploaded

### Build image

```sh
docker build -t ai-microservice .
```

### Run Image
```sh
docker run -d -p 8000:8000 --name ai-microservice ai-microservice
```


## 📡 API Usage

### Endpoint: `/preds`

**Method:** `POST`

### 🔹 Request Format

**Form Fields:**

- `text_field_1`: Any text input to check for offensive words.
- `text_field_2`: Additional text inputs are also processed.
- `files`: Images or videos to analyze for NSFW content.

**Example Request (Using cURL):**

```sh
curl -X POST "http://127.0.0.1:5000/preds" \
  -F "name=hello" \
  -F "comment=Buổi sáng thật cặc" \
  -F "files=@image.jpg" \
  -F "files=@video.mp4"
```

### 🔹 Response Format

```json
{
  "data": [
    {
      "field": "name",
      "offensive_words": [
        "ngu"
      ]
    },
    {
      "field": "description",
      "offensive_words": [
        "cặc"
      ]
    },
    {
      "field": "profile_picture",
      "filename": "hqdefault.jpg",
      "predictions": {
        "path": "./uploaded\\hqdefault.jpg",
        "isContainNude": false,
        "isContainViolence": false,
        "predicts": {
          "nude_score": 0,
          "violence_score": 50
        }
      }
    },
    {
      "field": "presentation_video",
      "filename": "fighting.mp4",
      "predictions": {
        "path": "./uploaded\\fighting.mp4",
        "type": "This video contains NSFW content",
        "timestamps": {
          "0:00:10": "Violence",
          "0:00:15": "Violence",
          "0:00:22": "Violence",
          "0:00:23": "Violence",
          "0:00:25": "Violence"
        }
      }
    }
  ]
}
```

## 🎯 Task & Hướng dẫn tối ưu khi triển khai lên server

### Task:
- Chuyển đổi toàn bộ sang API, loại bỏ UI.
- Tối ưu API để tăng tốc độ xử lý.
- Sử dụng đa luồng (threading) để xử lý song song các request.
- Tách riêng logic kiểm tra text, image, video để tối ưu hiệu năng.

### Khi triển khai lên server, cần thực hiện:
1. **Cài đặt Python, Docker, driver GPU (nếu có)** đầy đủ.
2. **Cài đặt Docker & NVIDIA Container Toolkit** nếu sử dụng GPU.
3. **Build lại Docker image sau mỗi lần cập nhật mã nguồn.**
4. **Chạy container với tham số phù hợp:**  
   - Nếu dùng GPU: `docker run --gpus all ...`
   - Nếu chỉ dùng CPU: `docker run ...`

## 📜 License

This project belong to https://hancity.vn
