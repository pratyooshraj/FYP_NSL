import cv2
import time
from collections import deque
from flask import Flask, Response, render_template
from ultralytics import YOLO

# Initialize the Flask app
app = Flask(__name__)

# Load the YOLO model (replace with your .pt file path)
model = YOLO('path_to_your_trained_model.pt')

# Initialize webcam (use '0' for default webcam)
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    raise RuntimeError("Error: Cannot access the webcam.")

# Queue to store detected letters
letter_queue = deque(maxlen=50)  # Store up to 50 letters

# A dictionary to store recent detections for each letter (for sliding window)
recent_detections = {}

# Define a time threshold for avoiding duplicate letters
time_threshold = 1.0  # Minimum time in seconds between consecutive same-letter additions

# Class mapping for detected letter IDs (update this with all your letters)
class_map = {
    0: 'अ', 1: 'आ', 2: 'इ', 3: 'ई', 4: 'उ', 5: 'ऊ',
    # Add all letter mappings here...
}


def generate_frames():
    """Generator function to yield video frames with YOLO detections."""
    confidence_threshold = 0.6  # Minimum confidence score to consider a detection
    sliding_window_size = 5  # Number of frames to average confidence scores

    while True:
        success, frame = cap.read()
        if not success:
            break

        # Run YOLO inference
        results = model(frame)

        # Annotate the frame with detections
        detected_letters = []
        for result in results:
            for box in result.boxes.xyxy:
                x1, y1, x2, y2 = map(int, box[:4])  # Bounding box coordinates
                confidence = float(box[4])  # Confidence score
                label = int(result.boxes.cls[0])  # Class ID

                # Map class ID to Nepali letter
                letter = class_map.get(label, '?')

                # Add detection to recent_detections
                if letter not in recent_detections:
                    recent_detections[letter] = []
                recent_detections[letter].append(confidence)

                # Keep only the last `sliding_window_size` confidence scores
                if len(recent_detections[letter]) > sliding_window_size:
                    recent_detections[letter].pop(0)

                # Calculate the average confidence for the letter
                avg_confidence = sum(recent_detections[letter]) / len(recent_detections[letter])

                # Only add letters with high average confidence
                if avg_confidence >= confidence_threshold:
                    # Check time threshold for duplicate letters
                    current_time = time.time()
                    if (
                            not letter_queue or
                            letter_queue[-1] != letter or
                            (recent_detections[letter][-1] and current_time - recent_detections[letter][
                                -1] > time_threshold)
                    ):
                        detected_letters.append(letter)
                        recent_detections[letter][-1] = current_time

                    # Draw the bounding box and label
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.putText(
                        frame, f"{letter} ({avg_confidence:.2f})",
                        (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2
                    )

        # Add high-confidence letters to the queue
        if detected_letters:
            letter_queue.extend(detected_letters)

        # Display the sentence being formed
        sentence = ''.join(letter_queue)
        cv2.putText(
            frame, f"Sentence: {sentence}",
            (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2
        )

        # Encode frame as JPEG
        _, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()


        # Yield the frame as a response
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    """Render the homepage."""
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    """Serve the video feed."""
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/get_sentence')
def get_sentence():
    """API endpoint to fetch the current sentence."""
    sentence = ''.join(letter_queue)
    return {'sentence': sentence}

if __name__ == '__main__':
    app.run(debug=True)
