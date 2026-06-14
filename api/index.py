from flask import Flask, request, jsonify
from flask_cors import CORS
import cv2
import numpy as np
import base64
import random
import os
from datetime import datetime

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

# ---------------------------------------------------------------------------
# Haar Cascade – loaded once at cold-start
# ---------------------------------------------------------------------------
_cascade_path = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
_face_cascade = cv2.CascadeClassifier(_cascade_path)


def detect_mask_in_frame(frame):
    """Heuristic mask detector using Haar Cascade + pixel-intensity scoring."""
    if frame is None or frame.size == 0:
        return {"detections": [], "count": 0, "confidence": 0,
                "masks_detected": 0, "no_masks_detected": 0}

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = _face_cascade.detectMultiScale(
        gray, scaleFactor=1.1, minNeighbors=3,
        minSize=(50, 50), maxSize=(600, 600)
    )

    detections, masks_detected, no_masks_detected, total_conf = [], 0, 0, 0

    for x, y, w, h in faces:
        gray_face = cv2.cvtColor(frame[y:y+h, x:x+w], cv2.COLOR_BGR2GRAY)
        lower_roi  = gray_face[int(h * 0.5):, :]
        lower_int  = np.mean(lower_roi)
        variance   = np.var(lower_roi)

        mask_score     = max(0, (110 - lower_int) / 30)
        variance_score = min(variance / 1000, 1.0)
        combined       = mask_score * 0.6 + variance_score * 0.4
        confidence     = float(np.clip(combined * 100 + random.uniform(-2, 2), 30, 99))
        confidence     = round(confidence, 1)
        has_mask       = confidence > 55

        if has_mask:
            masks_detected += 1
        else:
            no_masks_detected += 1
        total_conf += confidence

        detections.append({
            "label":         "MASK DETECTED" if has_mask else "NO MASK",
            "confidence":    confidence,
            "safety_status": "PROTECTED"      if has_mask else "UNSAFE",
            "has_mask":      bool(has_mask),
            "x": int(x), "y": int(y), "width": int(w), "height": int(h)
        })

    avg_conf = round(total_conf / len(detections), 1) if detections else 0.0
    return {
        "detections":       detections,
        "count":            int(len(detections)),
        "confidence":       float(avg_conf),
        "masks_detected":   int(masks_detected),
        "no_masks_detected": int(no_masks_detected)
    }


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({"status": "Backend running",
                    "timestamp": datetime.now().isoformat()}), 200


@app.route("/api/detect", methods=["POST"])
def detect_endpoint():
    """Live webcam detection — accepts base64 JPEG."""
    try:
        data = request.get_json()
        if not data or "image" not in data:
            return jsonify({"error": "No image data"}), 400

        image_b64 = data["image"]
        if "," in image_b64:
            image_b64 = image_b64.split(",")[1]

        image_bytes = base64.b64decode(image_b64)
        nparr  = np.frombuffer(image_bytes, np.uint8)
        frame  = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        if frame is None:
            return jsonify({"error": "Invalid image data"}), 400

        results = detect_mask_in_frame(frame)
        return jsonify({"success": True, **results}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/upload", methods=["POST"])
def upload_endpoint():
    """Static image upload detection."""
    try:
        if "file" not in request.files:
            return jsonify({"error": "No file provided"}), 400

        file = request.files["file"]
        if file.filename == "":
            return jsonify({"error": "No file selected"}), 400

        nparr = np.frombuffer(file.read(), np.uint8)
        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        if frame is None:
            return jsonify({"error": "Could not read image"}), 400

        results = detect_mask_in_frame(frame)
        return jsonify({"success": True, **results}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Vercel expects the module-level `app` object (WSGI)
