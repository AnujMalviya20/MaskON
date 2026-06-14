from flask import Flask, request, jsonify
from flask_cors import CORS
import cv2
import numpy as np
import base64
from datetime import datetime
from detect_mask import detect_mask_in_frame

app = Flask(__name__, static_folder='../frontend', static_url_path='/')
CORS(app, resources={r"/api/*": {"origins": "*"}})

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({
        'status': 'Backend running',
        'timestamp': datetime.now().isoformat()
    }), 200

@app.route('/api/detect', methods=['POST'])
def detect_endpoint():
    """Live webcam detection"""
    try:
        data = request.get_json()
        print(f'[API] Received detection request. Data keys: {list(data.keys()) if data else "None"}')
        
        if not data or 'image' not in data:
            print('[API] ERROR: No image data in request')
            return jsonify({'error': 'No image data'}), 400
        
        # Decode base64 image
        try:
            image_b64 = data['image']
            print(f'[API] Base64 image length: {len(image_b64)} chars')
            
            # Remove data URI prefix if present
            if ',' in image_b64:
                image_b64 = image_b64.split(',')[1]
                print(f'[API] Removed data URI prefix, new length: {len(image_b64)} chars')
            
            image_bytes = base64.b64decode(image_b64)
            print(f'[API] Decoded {len(image_bytes)} bytes')
            
            nparr = np.frombuffer(image_bytes, np.uint8)
            frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            
            if frame is None:
                print('[API] ERROR: cv2.imdecode returned None')
                return jsonify({'error': 'Invalid image data'}), 400
            
            print(f'[API] Frame decoded: shape={frame.shape}, dtype={frame.dtype}')
        except Exception as e:
            print(f'[API] ERROR decoding image: {str(e)}')
            return jsonify({'error': f'Failed to decode image: {str(e)}'}), 400
        
        # Detect masks
        print(f'[API] Starting mask detection...')
        results = detect_mask_in_frame(frame)
        print(f'[API] Detection complete: {results["count"]} faces detected')
        
        return jsonify({
            'success': True,
            'detections': results['detections'],
            'count': results['count'],
            'confidence': results['confidence'],
            'masks_detected': results['masks_detected'],
            'no_masks_detected': results['no_masks_detected']
        }), 200
    
    except Exception as e:
        print(f'[API] ERROR: {str(e)}')
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app.route('/api/upload', methods=['POST'])
def upload_endpoint():
    """Image upload detection"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Read file
        file_bytes = file.read()
        nparr = np.frombuffer(file_bytes, np.uint8)
        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if frame is None:
            return jsonify({'error': 'Could not read image'}), 400
        
        # Detect masks
        results = detect_mask_in_frame(frame)
        
        return jsonify({
            'success': True,
            'detections': results['detections'],
            'count': results['count'],
            'confidence': results['confidence'],
            'masks_detected': results['masks_detected'],
            'no_masks_detected': results['no_masks_detected']
        }), 200
    
    except Exception as e:
        print(f'Error: {str(e)}')
        return jsonify({'error': str(e)}), 500

@app.errorhandler(404)
def not_found(e):
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def server_error(e):
    return jsonify({'error': 'Server error'}), 500

if __name__ == '__main__':
    print('\n' + '='*60)
    print('🚀 SafeGuard AI - Real-Time Mask Detection Backend')
    print('='*60)
    print(f'📍 API Running on: http://127.0.0.1:5001')
    print(f'📍 Frontend URL: http://127.0.0.1:8000/live.html')
    print('✓ CORS enabled for all /api/* routes')
    print('✓ Face detection with Haar Cascades')
    print('✓ Logging enabled for all requests')
    print('Press CTRL+C to stop\n')
    print('='*60 + '\n')
    import os
    port = int(os.environ.get('PORT', 5001))
    app.run(debug=False, host='0.0.0.0', port=port, use_reloader=False)