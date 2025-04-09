from flask import Flask, render_template, Response, jsonify, request
import cv2
import threading
from gtts import gTTS  # Google TTS for MP3 generation
import os
from slr.main import process_frame
from slr.main import reset_detected_sentence  # Import reset function
from slr.main import delete_last_character  # Import delete function

app = Flask(__name__, template_folder="templates", static_folder="static")

detected_sentence = ""
camera_lock = threading.Lock()

def init_camera():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        raise RuntimeError("ERROR: Camera not accessible")
    return cap

cap = init_camera()

def generate_frames():
    global detected_sentence
    while True:
        with camera_lock:
            success, frame = cap.read()
            if not success:
                print("ERROR: Failed to capture frame")
                break

            processed_frame, current_sentence = process_frame(frame)
            detected_sentence = current_sentence
            
            _, buffer = cv2.imencode('.jpg', processed_frame)
            frame_data = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_data + b'\r\n')


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/app')
def app_page():
    return render_template('translator.html')

@app.route('/get_sentence')
def get_sentence():
    return jsonify({"sentence": detected_sentence})

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/clear_sentence', methods=['POST'])
def clear_sentence():
    """Clears the detected sentence globally"""
    global detected_sentence
    detected_sentence = ""  # Reset in app.py
    reset_detected_sentence()  # Reset in main.py
    return jsonify({"status": "success", "message": "Sentence cleared!"})

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/delete_last_character', methods=['POST'])
def delete_last():
    from slr.main import delete_last_character
    global detected_sentence
    detected_sentence = detected_sentence[:-1] 
    delete_last_character()
    return jsonify({'message': 'Last character deleted', 'sentence': detected_sentence})

@app.route('/speak', methods=['POST'])
def speak():
    """Convert detected sentence to speech and return audio file URL"""
    global detected_sentence

    if not detected_sentence.strip():
        return jsonify({"status": "error", "message": "No sentence to speak"})

    # Convert text to speech and save as MP3
    tts = gTTS(detected_sentence)
    
    # Make sure the audio directory exists
    os.makedirs("static/audio", exist_ok=True)
    
    audio_path = "static/audio/speech.mp3"
    tts.save(audio_path)

    return jsonify({"status": "success", "audio_url": "/" + audio_path})



if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0', port=5000, debug=True)
    finally:
        with camera_lock:
            cap.release()