# pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
import tkinter as tk
from tkinter import Label
from PIL import Image, ImageTk
import torch
import cv2
from torch.cuda import is_available

# Load the YOLOv5 model (use GPU if available)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = torch.hub.load('ultralytics/yolov5', 'custom', path='best.pt', device=device)  # Adjust path if necessary


# Initialize the main application
class RealTimeDetectionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("YOLOv5 Real-Time Detection with GPU")

        # Create a label to display the video feed
        self.video_label = Label(root)
        self.video_label.pack()

        # Capture video from the laptop camera
        self.cap = cv2.VideoCapture(0)

        # Start video stream
        self.update_frame()

        # Handle window close event
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def update_frame(self):
        ret, frame = self.cap.read()
        if ret:
            # Convert BGR to RGB for PIL
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Run YOLOv5 model on the frame
            results = model(rgb_frame)
            results.render()  # Draw bounding boxes on the image

            # Convert numpy array (with bounding boxes) to PIL Image
            frame_with_boxes = Image.fromarray(results.imgs[0])

            # Convert PIL image to ImageTk for tkinter
            imgtk = ImageTk.PhotoImage(image=frame_with_boxes)

            # Update the label with the new frame
            self.video_label.imgtk = imgtk
            self.video_label.configure(image=imgtk)

        # Schedule the next frame update
        self.root.after(10, self.update_frame)

    def on_closing(self):
        self.cap.release()
        self.root.destroy()


# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = RealTimeDetectionApp(root)
    root.mainloop()
