import tkinter as tk
from tkinter import messagebox
import cv2
from PIL import Image, ImageTk
import datetime
from gtts import gTTS
import os
import torch
import time
import threading
from collections import defaultdict

import pathlib
from pathlib import Path
pathlib.PosixPath = pathlib.WindowsPath

import warnings
warnings.simplefilter("ignore", category=FutureWarning)

from gesture_mapping import consonants_mapping, vowels_mapping, consonant_vowel_matrix

os.environ['TORCH_HOME'] = "D:/Programming/FYP_NSL/cache"


class SignAlphabetApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Nepali Sign Alphabet Detection")
        self.root.geometry("900x700")
        self.root.resizable(False, False)

        self.text_box = tk.Text(root, height=1, width=43, wrap="word", font=("Noto Sans Devanagari", 25))
        self.text_box.grid(row=0, column=0, columnspan=3, padx=10, pady=10)

        self.clear_button = tk.Button(root, text="Clear", command=self.clear_textbox, font=("Arial", 14))
        self.clear_button.grid(row=0, column=3, padx=10, pady=10, sticky="e")

        self.video_display = tk.Label(root, bg="black")
        self.video_display.grid(row=1, column=0, columnspan=4, padx=10, pady=10)

        # buttons
        self.button_frame = tk.Frame(root)
        self.button_frame.grid(row=2, column=0, columnspan=4, pady=20)

        self.start_button = tk.Button(self.button_frame, text="Start", command=self.start_video, font=("Arial", 12), width=12)
        self.start_button.grid(row=0, column=0, padx=10)

        self.stop_button = tk.Button(self.button_frame, text="Stop", command=self.stop_video, font=("Arial", 12),width=12, state=tk.DISABLED)
        self.stop_button.grid(row=0, column=1, padx=10)

        self.process_button = tk.Button(self.button_frame, text="Process", command=self.process_text,font=("Arial", 12), width=12)
        self.process_button.grid(row=0, column=2, padx=10)

        self.save_button = tk.Button(self.button_frame, text="Save", command=self.save_text, font=("Arial", 12),width=12)
        self.save_button.grid(row=0, column=3, padx=10)

        self.speak_button = tk.Button(self.button_frame, text="Speak", command=self.speak_text, font=("Arial", 12),width=12)
        self.speak_button.grid(row=0, column=4, padx=10)

        self.model = torch.hub.load("ultralytics/yolov5", "custom",path="D:/Programming/cuda_test/yolov5/all_model.pt").half().to("cuda")

        self.cap = None  # Camera feed will be initialized on start
        self.running = False
        self.video_thread = None

        self.rolling_window = 4  # 4-second detection window
        self.start_time = time.time()
        self.detections = defaultdict(lambda: {"count": 0, "confidence_sum": 0.0})

    def start_video(self):
        if not self.running:
            self.cap = cv2.VideoCapture(0)
            self.running = True
            self.video_thread = threading.Thread(target=self.update_video_feed)
            self.video_thread.start()
            self.start_button.config(state=tk.DISABLED)
            self.stop_button.config(state=tk.NORMAL)
            self.start_time = time.time()

    def stop_video(self):
        if self.running:
            self.running = False
            if self.cap:
                self.cap.release()
                self.cap = None
            self.video_display.config(image='')
            self.start_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.DISABLED)

    def update_video_feed(self):
        while self.running:
            success, frame = self.cap.read()
            if not success:
                continue

            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.model(rgb_frame)

            for detection in results.xyxy[0]:
                x1, y1, x2, y2, confidence, cls = detection.tolist()
                class_name = self.model.names[int(cls)]

                if confidence > 0.3:
                    self.detections[class_name]["count"] += 1
                    self.detections[class_name]["confidence_sum"] += confidence

                    cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
                    cv2.putText(frame, f"{class_name} {confidence:.2f}", (int(x1), int(y1) - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

            img = Image.fromarray(rgb_frame)
            imgtk = ImageTk.PhotoImage(image=img)
            self.video_display.imgtk = imgtk
            self.video_display.configure(image=imgtk)

            if time.time() - self.start_time >= self.rolling_window:
                self.update_text_box()
                self.start_time = time.time()

    def update_text_box(self):
        """ Updates the text box with the most detected character every 4 seconds. """
        if self.detections:
            most_detected_class = max(self.detections, key=lambda x: self.detections[x]["count"])
            avg_confidence = self.detections[most_detected_class]["confidence_sum"] / self.detections[most_detected_class]["count"]

            if avg_confidence > 0.3:
                nepali_char = vowels_mapping.get(most_detected_class, consonants_mapping.get(most_detected_class, ""))
                if nepali_char:
                    self.text_box.insert(tk.END, nepali_char)

        self.detections.clear()

    def clear_textbox(self):
        self.text_box.delete("1.0", tk.END)

    def process_text(self):
        text = self.text_box.get("1.0", tk.END).strip()
        processed_text = []

        i = 0
        while i < len(text):
            current_char = text[i]

            if current_char in consonants_mapping.values():
                if i + 1 < len(text) and text[i + 1] in vowels_mapping.values():
                    consonant = list(consonants_mapping.keys())[list(consonants_mapping.values()).index(current_char)]
                    vowel = text[i + 1]

                    if vowel in consonant_vowel_matrix:
                        combined = consonant_vowel_matrix[vowel].get(consonant, None)
                        if combined:
                            processed_text.append(combined)
                            i += 2  # Skip the next vowel as it's part of the combination
                        else:
                            processed_text.append(current_char)
                            i += 1
                    else:
                        processed_text.append(current_char)
                        i += 1
                else:
                    processed_text.append(current_char)
                    i += 1
            else:
                processed_text.append(current_char)
                i += 1

        self.text_box.delete("1.0", tk.END)
        self.text_box.insert("1.0", ''.join(processed_text))

    def save_text(self):
        self.process_text()
        text = self.text_box.get("1.0", tk.END).strip()

        if text:
            filename = f"{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}_text.txt"
            with open(filename, "w", encoding="utf-8") as file:
                file.write(text)
            messagebox.showinfo("Save", f"Text saved successfully as {filename}!")
        else:
            messagebox.showwarning("Save", "No text to save!")

    def speak_text(self):
        self.stop_video()
        self.process_text()
        text = self.text_box.get("1.0", tk.END).strip()

        if text:
            try:
                current_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                speech_filename = f"{current_time}.mp3"
                tts = gTTS(text, lang='ne')
                tts.save(speech_filename)
                os.system(f"start {speech_filename}")
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {e}")
        else:
            messagebox.showwarning("Speak", "No text to speak!")

    def on_closing(self):
        self.running = False
        self.stop_video()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = SignAlphabetApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()
