# MaskVision AI
# MaskVision AI

A local, privacy-preserving web application for detecting face masks in images and live webcam streams. The backend uses Flask and OpenCV (Haar cascades) for face detection with a lightweight heuristic-based mask indicator. The frontend is a single-page UI that supports live monitoring and image uploads.

This README contains everything you need to run the project locally on macOS (zsh).

---

## Table of contents
- Quick start
- Requirements
- Setup (recommended)
- Run (backend + frontend)
- API reference
- Frontend usage
- Troubleshooting
- Development notes
- Contributing
- License

---

## Quick start
1. Clone the repository and open the project folder:

    ```bash
    git clone <your-repo-url> maskvision-ai
    cd maskvision-ai
    ```

2. Create a Python 3.11 virtual environment and install backend dependencies:

    ```bash
    /usr/local/bin/python3.11 -m venv backend/venv
    source backend/venv/bin/activate
    pip install --upgrade pip setuptools wheel
    pip install -r backend/requirements.txt
    ```

3. Start the backend and frontend in two separate terminals:

    Backend:
    ```bash
    cd backend
    source venv/bin/activate
    python app.py
    ```

    Frontend (static server):
    ```bash
    cd frontend
    python3 -m http.server 8000
    ```

4. Open the live monitor in your browser:

    - Frontend: http://localhost:8000/live.html
    - Backend health: http://127.0.0.1:5000/api/health

---

## Requirements
- macOS (tested)
- Python 3.11 (recommended)
- pip
- A modern browser (Chrome, Firefox, Safari) with webcam permissions enabled for live mode

Notes:
- OpenCV and numpy wheels may require a compatible Python version. If you run into build errors, ensure the virtualenv uses Python 3.11.

---

## Setup (recommended)
- Use the included `backend/requirements.txt` to install dependencies inside a dedicated virtual environment.
- If you prefer Docker, I can add a `Dockerfile` and `docker-compose.yml` on request to containerize both the backend and a static file server for the frontend.

---

## Run
- Backend (Flask API):
   - The backend serves the API on `http://127.0.0.1:5000` and the frontend static files are in the `frontend` folder (not served by the backend in development).
   - Start it with `python app.py` from the `backend` folder (with venv activated).

- Frontend (static):
   - Serve the `frontend` folder using Python's simple HTTP server so webcam pages load correctly:
   - `python3 -m http.server 8000` from the `frontend` folder.

---

## API reference
- GET /api/health
   - Health check. Response:
      ```json
      { "status": "Backend running", "timestamp": "..." }
      ```

- POST /api/detect
   - Live detection endpoint.
   - Body: `{ "image": "data:image/jpeg;base64,..." }`
   - Response:
      ```json
      {
         "success": true,
         "detections": [ { "label": "MASK DETECTED", "confidence": 85.1, "has_mask": true, "x": 10, "y": 20, "width": 100, "height": 120 } ],
         "count": 1,
         "confidence": 85.1,
         "masks_detected": 1,
         "no_masks_detected": 0
      }
      ```

- POST /api/upload
   - Multipart form upload (file field `file`) - returns the same shape response as `/api/detect`.

---

## Frontend usage
- Open `http://localhost:8000/live.html` and click "Start Monitoring".
- Allow camera access when prompted.
- The UI will call `/api/detect` every ~400ms while running and show a single persistent alert when any face without mask is detected.
- Use `upload.html` to test image uploads.

---

## Troubleshooting
- cv2 Haar cascade not found / face detection failing:
   - The code prints lifecycle messages on startup (cascade path and OK/ERROR). Confirm you started the backend with the same venv where `opencv-python` is installed.
- `pip install` errors for numpy/opencv:
   - Use Python 3.11 for the venv as many wheels are prebuilt for that version. Install `python@3.11` with Homebrew if needed: `brew install python@3.11`.
- Browser denies camera access:
   - Make sure you are serving the page over `http://` (not `file://`) and that you allow camera permissions.

---

## Development notes
- `backend/app.py` - Flask app and endpoints.
- `backend/detect_mask.py` - Face detection and mask heuristic. Uses OpenCV Haar cascades and a lightweight scoring heuristic.
- `frontend/` - Static UI. Key files:
   - `live.html` - Live monitoring and detection logic
   - `upload.html` - Image upload
   - `css/style.css` - Styles
   - `js/app.js` - Utility helpers

---

## Contributing
- Fork the repo, create a feature branch, test locally, and open a PR with a clear description.
- If you want CI or Docker support added, open an issue and I can implement it.

---

## License
This project is provided as-is for educational/demo purposes. Add a license file (MIT or similar) if you want to publish it.

---

If you want, I can:
- Add `start` scripts (Makefile or shell scripts) to simplify running both servers.
- Add Docker support with `docker-compose`.
- Improve the detection algorithm or replace it with a small neural model.

Tell me which of those you'd like next and I'll implement it.
## Project Overview
MaskVision AI is a deep learning and computer vision-based web application designed to detect whether a person is wearing a face mask. The application utilizes a pre-trained MobileNetV2 model for mask detection and provides real-time feedback through a modern user interface. Users can access live webcam detection or upload images for mask detection.

## Features
- **Live Face Mask Detection**: Access the webcam to detect if a person is wearing a mask in real-time.
- **Image Upload Detection**: Users can upload images to check for mask compliance.
- **Alert System**: Warning messages and alert sounds are triggered when no mask is detected.
- **Modern UI**: A sleek, dark-themed interface with responsive design and smooth animations.
- **Dashboard**: Displays total detections, mask count, no-mask count, and last detection status.

## Installation
To set up the project, follow these steps:

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/maskvision-ai.git
   cd maskvision-ai
   ```

2. Navigate to the backend directory and install the required packages:
   ```
   cd backend
   pip install -r requirements.txt
   ```

3. Ensure you have the necessary environment variables set up in a `.env` file based on the `.env.example` template.

## Run Commands
To run the application, execute the following commands:

1. Start the Flask backend:
   ```
   python app.py
   ```

2. Open the frontend in your web browser:
   ```
   open frontend/index.html
   ```

## Screenshots
(Include screenshots of the application here)

## Technologies Used
- **Frontend**: HTML5, CSS3, JavaScript
- **Backend**: Python Flask, Flask-CORS
- **AI/Computer Vision**: TensorFlow, Keras, OpenCV, NumPy
- **Model**: MobileNetV2 (pre-trained)

## Future Scope
- Implement user authentication for personalized experiences.
- Enhance the model with more training data for improved accuracy.
- Add support for multiple languages in the user interface.
- Expand the alert system with customizable notifications.