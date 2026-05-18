# SafeGuard AI - GitHub Setup Guide

Your project is now live on GitHub! Here's how to clone and run it on a different PC.

## Repository Information
- **GitHub URL**: https://github.com/AnujMalviya20/MaskON.git
- **Branch**: main
- **Last Updated**: May 18, 2026

---

## Quick Start (Any OS)

### Step 1: Clone the Repository
```bash
git clone https://github.com/AnujMalviya20/MaskON.git
cd MaskON
```

### Step 2: Set Up Environment

#### On Windows (PowerShell or CMD):
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate

# Install dependencies
pip install -r backend/requirements.txt
```

#### On macOS/Linux:
```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r backend/requirements.txt
```

### Step 3: Run the Application

#### Start Backend (Flask API):
```bash
cd backend
python app.py
```
Backend will be available at: `http://127.0.0.1:5000`

#### Start Frontend (in a new terminal):
```bash
cd frontend
# Windows
python -m http.server 8000

# macOS/Linux
python3 -m http.server 8000
```
Frontend will be available at: `http://127.0.0.1:8000/live.html`

### Step 4: Open in Browser
Navigate to: **http://localhost:8000/live.html**

Click "Start Monitoring" and allow camera access.

---

## System Requirements

- **OS**: Windows 10+, macOS 10.14+, Ubuntu 18.04+
- **Python**: 3.8 or higher
- **RAM**: 4GB minimum
- **Camera**: Any USB or built-in webcam
- **Browser**: Chrome, Firefox, Safari, Edge (modern version)

---

## Project Structure

```
MaskON/
├── backend/
│   ├── app.py                          # Flask API server
│   ├── detect_mask.py                  # Face detection & mask classification
│   ├── requirements.txt                # Python dependencies
│   └── model/                          # Pre-trained models (optional)
├── frontend/
│   ├── live.html                       # Real-time detection dashboard
│   ├── index.html                      # Home page
│   ├── upload.html                     # Image upload analysis
│   ├── about.html                      # About page
│   ├── css/
│   │   └── style.css                   # Professional dark theme styling
│   ├── js/
│   │   ├── script.js                   # Utility functions
│   │   └── app.js                      # Navigation logic
│   └── assets/
│       └── sounds/
│           └── alert.mp3               # Alert notification sound
├── README.md                           # Project documentation
├── SETUP_GUIDE.md                      # Detailed setup instructions
├── GITHUB_SETUP.md                     # This file
└── .gitignore                          # Git ignore rules
```

---

## Features

✅ **Real-Time Detection**
- Live webcam feed with 24-30 FPS smooth rendering
- Square 640x640 video canvas for consistent overlay mapping

✅ **Mask Detection**
- OpenCV Haar Cascades for accurate face detection
- Mask/No-Mask classification with confidence scores
- Green bounding boxes = Mask detected
- Red bounding boxes = No mask detected

✅ **Live Alerts**
- Real-time notifications when mask status changes
- Color-coded alerts (green = safe, red = warning)
- Persistent status display

✅ **Professional Dashboard**
- Real-time FPS counter
- Detection latency monitoring
- Session uptime tracking
- Detection statistics (faces, masks, confidence)

✅ **Responsive Design**
- Works on desktop and mobile browsers
- Professional dark theme (#0a0e27 primary)
- Cyan (#00d9ff) and green (#00ff99) accents

---

## API Endpoints

### POST `/api/detect`
Send a frame for real-time mask detection.

**Request:**
```json
{
  "image": "data:image/jpeg;base64,/9j/4AAQSkZJRg..."
}
```

**Response:**
```json
{
  "success": true,
  "detections": [
    {
      "x": 100,
      "y": 150,
      "width": 200,
      "height": 250,
      "confidence": 87.5,
      "has_mask": true,
      "label": "MASK DETECTED",
      "safety_status": "PROTECTED"
    }
  ],
  "count": 1,
  "confidence": 87.5,
  "masks_detected": 1,
  "no_masks_detected": 0
}
```

### GET `/api/health`
Check backend health status.

**Response:**
```json
{
  "status": "Backend running",
  "timestamp": "2026-05-18T13:00:00.000000"
}
```

---

## Configuration

### Environment Variables (.env)
Create a `.env` file in the project root:

```env
# Flask Configuration
FLASK_ENV=development
FLASK_DEBUG=True

# API Configuration
API_PORT=5000
API_HOST=127.0.0.1

# CORS Configuration
CORS_ORIGINS=*

# Detection Sensitivity
SCALE_FACTOR=1.1
MIN_NEIGHBORS=3
MIN_FACE_SIZE=50
MAX_FACE_SIZE=600

# Detection Confidence Threshold
CONFIDENCE_THRESHOLD=55
```

---

## Troubleshooting

### Port Already in Use
If port 5000 or 8000 is already in use:

**Windows:**
```powershell
netstat -ano | findstr :5000
taskkill /PID <PID> /F
```

**macOS/Linux:**
```bash
lsof -i :5000
kill -9 <PID>
```

### Camera Not Working
1. Check browser permissions: Settings → Privacy → Camera
2. Try a different browser (Chrome works best)
3. Restart the application
4. Check if camera is being used by another app

### No Face Detection
1. Ensure good lighting
2. Face should be at least 50x50 pixels
3. Check that cascade file loaded (check Flask logs)
4. Try adjusting `SCALE_FACTOR` and `MIN_NEIGHBORS` in `.env`

### High Latency
1. Close unnecessary browser tabs
2. Check network bandwidth
3. Reduce image quality (JPEG quality setting in live.html)
4. Use a faster machine

---

## Development Tips

### Enable Debug Mode
Edit `backend/app.py`:
```python
app.run(debug=True, host='127.0.0.1', port=5000)
```

### Check Flask Logs
The backend prints detailed debugging information:
```
[DEBUG] Loading Haar Cascade from: ...
[DEBUG] Processing frame: shape=(640,640,3)
[DEBUG] Faces detected: 1
[DEBUG] Final: 1 faces, 1 with mask
```

### Browser Console Logs
Open DevTools (F12) → Console tab to see frontend detection calls:
```javascript
// Detection API calls logged automatically
// Watch for POST /api/detect requests
```

---

## Performance Optimization

### Backend
- Face detection runs on CPU (OpenCV Haar Cascades)
- Optimized detection parameters for 400ms throttle
- JSON serialization fixed for NumPy compatibility

### Frontend
- requestAnimationFrame() for smooth 30 FPS video rendering
- Throttled detection API calls (400ms interval, not every frame)
- Canvas object-fit: cover for consistent aspect ratio
- Lightweight overlay drawing with minimal operations

### Recommended Settings
- Video resolution: 640x640
- Detection frequency: 400ms (2.5 detections/second)
- JPEG quality: 0.8 (80%)
- Canvas size: 640x640 (square for proper overlay mapping)

---

## Contributing

To contribute improvements:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Make changes and commit: `git commit -am 'Add feature'`
4. Push to branch: `git push origin feature/your-feature`
5. Submit a pull request

---

## License

This project is open source and available under the MIT License.

---

## Support

For issues, questions, or suggestions:
1. Check the troubleshooting section above
2. Review detailed logs in Flask console
3. Check browser DevTools console (F12)
4. Open an issue on GitHub: https://github.com/AnujMalviya20/MaskON/issues

---

## Version Information

- **SafeGuard AI**: v1.0.0
- **Release Date**: May 18, 2026
- **Python Version**: 3.8+
- **OpenCV**: 4.8.0+
- **Flask**: 2.3.3+

---

## What's Included

✅ Complete source code (frontend + backend)
✅ Pre-trained Haar Cascade classifier
✅ Alert sound file (alert.mp3)
✅ Professional CSS styling with dark theme
✅ Comprehensive documentation
✅ Setup guides for all platforms
✅ Example configuration files

---

**Happy detecting! 🚀**

For the latest updates and features, visit: https://github.com/AnujMalviya20/MaskON
