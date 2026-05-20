# MaskVision AI

#Overview
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
