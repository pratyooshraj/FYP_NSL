import tkinter as tk
from tkinter import messagebox, scrolledtext
from tkinter import filedialog
import cv2
from PIL import Image, ImageTk
import uuid
from ultralytics import YOLO  # Assuming YOLOv5/YOLOv8
import threading
from collections import deque

class GestureRecognitionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gesture Recognition App")
        self.root.geometry("800x700")

        # Initialize YOLO model
        # self.model = YOLO("path_to_yolo_model.pt")  # Update with your YOLO model path
        self.model=""
        # Video Capture variables
        self.cap = None
        self.video_running = False

        # Sentence tracking
        self.sentence = ""
        self.gesture_queue = deque(maxlen=20)  # A queue to store the last gestures

        # UI Elements
        self.video_label = tk.Label(self.root, text="Video Feed", bg="black")
        self.video_label.pack(fill="both", expand=True)

        self.control_frame = tk.Frame(self.root)
        self.control_frame.pack(pady=10)

        self.start_button = tk.Button(self.control_frame, text="Start Video", command=self.start_video)
        self.start_button.grid(row=0, column=0, padx=10)

        self.capture_button = tk.Button(self.control_frame, text="Capture Gesture", command=self.capture_gesture, state="disabled")
        self.capture_button.grid(row=0, column=1, padx=10)

        self.stop_button = tk.Button(self.control_frame, text="Stop Video", command=self.stop_video, state="disabled")
        self.stop_button.grid(row=0, column=2, padx=10)

        self.exit_button = tk.Button(self.control_frame, text="Exit", command=self.exit_app)
        self.exit_button.grid(row=0, column=3, padx=10)

        self.log_area = scrolledtext.ScrolledText(self.root, height=10)
        self.log_area.pack(fill="x", padx=10, pady=10)

        # Sentence display area
        self.sentence_label = tk.Label(self.root, text="Sentence: ", font=("Helvetica", 16), bg="white", anchor="w")
        self.sentence_label.pack(fill="x", padx=10, pady=10)

        # Thread for video processing
        self.thread = None

    def start_video(self):
        self.cap = cv2.VideoCapture(0)  # 0 for webcam; update for video file if needed
        if not self.cap.isOpened():
            messagebox.showerror("Error", "Unable to access the camera.")
            return

        self.video_running = True
        self.capture_button.config(state="normal")
        self.stop_button.config(state="normal")
        self.start_button.config(state="disabled")
        self.thread = threading.Thread(target=self.update_frame)
        self.thread.start()

    def update_frame(self):
        pass
        while self.video_running:
            ret, frame = self.cap.read()
            if not ret:
                self.log_message("Failed to read frame from the camera.")
                break

            # YOLO Inference
            results = self.model(frame)
            for result in results[0].boxes:
                # Assuming your model returns bounding boxes and labels
                x1, y1, x2, y2 = map(int, result.xyxy[0])  # Coordinates
                label = result.cls  # Class label
                confidence = result.conf  # Confidence score

                # Draw bounding box and label
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(frame, f"{label} {confidence:.2f}", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

                # Update sentence and gesture queue
                self.update_sentence(label)

            # Convert BGR to RGB and update the Tkinter label
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame)
            imgtk = ImageTk.PhotoImage(image=img)
            self.video_label.imgtk = imgtk
            self.video_label.configure(image=imgtk)

        self.video_running = False

    def capture_gesture(self):
        if self.cap and self.video_running:
            ret, frame = self.cap.read()
            if ret:
                # Save captured frame
                unique_id = uuid.uuid4().hex
                filename = f"gesture_{unique_id}.jpg"
                cv2.imwrite(filename, frame)
                self.log_message(f"Gesture captured and saved as {filename}")
            else:
                self.log_message("Failed to capture gesture.")

    def update_sentence(self, gesture_label):
        """
        Update the sentence based on the detected gesture.
        """
        self.gesture_queue.append(gesture_label)  # Add gesture to the queue
        self.sentence = " ".join(list(self.gesture_queue))  # Form the sentence
        self.sentence_label.config(text=f"Sentence: {self.sentence}")  # Update the GUI

    def stop_video(self):
        self.video_running = False
        if self.cap:
            self.cap.release()
        self.video_label.configure(image="")
        self.capture_button.config(state="disabled")
        self.stop_button.config(state="disabled")
        self.start_button.config(state="normal")

    def exit_app(self):
        self.video_running = False
        if self.cap:
            self.cap.release()
        self.root.destroy()

    def log_message(self, message):
        self.log_area.insert(tk.END, message + "\n")
        self.log_area.see(tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = GestureRecognitionApp(root)
    root.mainloop()
