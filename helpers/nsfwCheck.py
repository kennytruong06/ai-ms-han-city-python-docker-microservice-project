import datetime
import cv2
import os
import uuid
from helpers.nudityDetection import nude_detection
from helpers.violenceDetection import violence_detection
from config.config import TEMP_DIR


def nsfw_check(img_path):
    """
    Kiểm tra mức độ NSFW của hình ảnh và xác định có chứa nội dung không phù hợp hay không.

    PARAMS::
    - img_path: Đường dẫn đến ảnh cần kiểm tra.

    RETURNS::
    - predicts: Dictionary chứa điểm số NSFW (nude, violence, natural).
    - isContainNude: Boolean - True nếu ảnh chứa nội dung khỏa thân (nude).
    - isContainViolence: Boolean - True nếu ảnh có nội dung bạo lực (violence).
    """
    # Lấy kết quả từ các mô hình detection
    nude_score = nude_detection(img_path)
    violence_score = violence_detection(img_path)
    # Giả sử trả về mảng [[drugs, violence, natural]]
    # nsfw_preds = violence_detection(img_path)

    predicts = {
        'nude_score': int(nude_score[img_path]['unsafe'] * 100),
        'violence_score': int(violence_score * 100)
        # 'violence_score': int(nsfw_preds[0][1] * 100),
        # 'natural_score': int(nsfw_preds[0][2] * 100)
    }

    return {
        "path": img_path,
        "isContainNude": predicts['nude_score'] > 85,
        "isContainViolence": predicts['violence_score'] > 60, # and predicts['natural_score'] < 25,
        "predicts": predicts,
    }


def nsfw_check_video(video_path, frame_skip=30):
    """
    Phát hiện NSFW trong video (nude hoặc bạo lực) và dừng khi gặp nội dung đầu tiên.

    PARAMS::
    - video_path: Đường dẫn tới video cần kiểm tra.
    - frame_skip: Số frame bỏ qua (ví dụ: mỗi 30 frame kiểm tra 1 frame).

    RETURNS::
    - dict: {
        path: str,
        type: str,
        timestamps: Optional[dict] nếu phát hiện NSFW
    }
    """
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        return {
            "path": video_path,
            "type": "Cannot open video."
        }

    fps = int(cap.get(cv2.CAP_PROP_FPS))
    frame_count = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        if frame_count % frame_skip == 0:
            temp_path = os.path.join(TEMP_DIR, f"{uuid.uuid4().hex[:8]}.jpg")
            cv2.imwrite(temp_path, frame)

            nsfw_result = nsfw_check(temp_path)
            os.remove(temp_path)  # Xoá frame tạm ngay

            if nsfw_result["isContainNude"] or nsfw_result["isContainViolence"]:
                formatted_time = str(datetime.timedelta(seconds=frame_count / fps))
                cap.release()
                return {
                    "path": video_path,
                    "type": "This video contains NSFW content",
                    "timestamps": {
                        formatted_time: "Nude" if nsfw_result["isContainNude"] else "Violence"
                    }
                }

        frame_count += 1

    cap.release()
    return {
        "path": video_path,
        "type": "This video is safe!"
    }
