# Hancity AI Microservice (AI MS)

## 📌 Introduction

This is the AI microservice developed by Hancity, designed to provide automated content moderation APIs 
for post submission systems. It uses AI models to detect sensitive content (NSFW), violence in images and videos, 
and offensive language in text. The service is designed to run without a user interface (UI) 
and is fully accessible via RESTful API endpoints, making it easy to integrate into any backend system.

## 🚀 Features

- **Detect offensive words** in text inputs using a predefined list of negative words.
- **Analyze images** to determine NSFW content using NudeNet and ViT Base Violence Detection.
- **Analyze videos** by extracting frames and checking for NSFW content.
- **Support multiple file uploads:** PNG, JPG, JPEG, MP4, AVI, MOV, MKV.
- **REST API interface** for easy integration.
- **Secure file handling**, processing, and automatic deletion after analysis.

## 🛠 Installation (How to run by docker)

### Build image

```sh
DOCKER_BUILDKIT=1 docker-compose build
```

### Create docker network

```sh
docker network create han.city.network
```

### Run Image
```sh
DOCKER_BUILDKIT=1 docker-compose up -d
```

## 📡 API Usage

### Endpoint: `/api/moderation/check`

**Method:** `POST`

### 🔹 Request Format

**Form Fields:**

JSON Fields:

- `content`: A list of text strings to be checked for offensive words.
- `pictures`: A list of image URLs (or local paths) to be analyzed for NSFW or violent content.
- `videos`: A list of video URLs (or local paths) to be analyzed for NSFW or violent content.

**Example Request (Using cURL):**

```sh
curl --location 'http://localhost:8000/api/moderation/check' \
--header 'Content-Type: application/json' \
--data '{
    "content": [
        "Tôi là 1 người tốt lồn", "Hôm nay trời thật cặc", "Con đĩ mẹ mày nữa"
    ],
    "pictures": [
        "https://hoseiki.vn/wp-content/uploads/2025/03/meo-cute-14.jpg?v=1741737378"
    ],
    "videos": [
        "https://down-bs-sg.vod.susercontent.com/api/v4/11110103/mms/vn-11110103-6khw9-m37nrf6m9d646f.16000051732959709.mp4"
    ]
}'
```

### 🔹 Response Format

```json
{
    "data": [
        {
            "field": "content",
            "offensive_words": [
                "lồn",
                "cặc",
                "đĩ"
            ]
        },
        {
            "field": "pictures",
            "results": [
                {
                    "source": "https://hoseiki.vn/wp-content/uploads/2025/03/meo-cute-14.jpg?v=1741737378",
                    "predictions": {
                        "path": "/app/storage/downloaded/1780c835.jpg",
                        "isContainNude": false,
                        "isContainViolence": true,
                        "predicts": {
                            "nude_score": 0.0,
                            "violence_score": 66.0
                        }
                    },
                    "error": null
                }
            ]
        },
        {
            "field": "videos",
            "results": [
                {
                    "source": "https://down-bs-sg.vod.susercontent.com/api/v4/11110103/mms/vn-11110103-6khw9-m37nrf6m9d646f.16000051732959709.mp4",
                    "predictions": {
                        "path": "/app/storage/downloaded/42308006.mp4",
                        "type": "This video contains NSFW content",
                        "timestamps": {
                            "0:00:03.600000": "Nude"
                        }
                    },
                    "error": null
                }
            ]
        }
    ]
}
```

## 🎯 Task & Optimization Guide for Deployment

### Task:

- Convert the entire project to API-only, remove UI ✅
- Optimize API for better processing speed ✅
- Use multithreading to handle concurrent requests ✅
- Separate logic for text, image, and video moderation to improve performance ✅

### Deployment Checklist:
1. **Install Python, Docker, and GPU drivers (if applicable).**
2. **Install Docker & NVIDIA Container Toolkit if using GPU acceleration.**
3. **Rebuild the Docker image every time you update the source code.**
4. **Run the container with appropriate options:**
   - If using GPU:docker run --gpus all ...
   - If using CPU only: docker run ...

## 📜 License

This project belong to https://hancity.vn
