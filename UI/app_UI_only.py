import tkinter as tk
from tkinter import messagebox
import cv2
from PIL import Image, ImageTk
import datetime
from gtts import gTTS
import os

from gesture_mapping import consonants_mapping, vowels_mapping, consonant_vowel_matrix


class SignAlphabetApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Nepali Sign Alphabet Detection")
        self.root.geometry("900x700")  # Adjusted size
        self.root.resizable(False, False)

        self.text_box = tk.Text(root, height=1, width=43, wrap="word", font=("Noto Sans Devanagari", 25))
        self.text_box.grid(row=0, column=0, columnspan=3, padx=10, pady=10)
        self.text_box.insert("1.0", "नेपाली भाषा समर्थन गरिएको छ। हरइयओ कआअपई")
        # self.text_box.insert("1.0", "नेपाली भाषा")
        # self.text_box.insert("1.0", "हरइयओ")
        # self.text_box.insert("1.0", "अ")
        # Clear Button
        self.clear_button = tk.Button(root, text="Clear", command=self.clear_textbox, font=("Arial", 14))
        self.clear_button.grid(row=0, column=3, padx=10, pady=10, sticky="e")

        # Video Display (adjusted to dynamically match the camera feed)
        self.video_display = tk.Label(root, bg="black")
        self.video_display.grid(row=1, column=0, columnspan=4, padx=10, pady=10)

        # Modern Layout for Bottom Buttons
        self.button_frame = tk.Frame(root)
        self.button_frame.grid(row=2, column=0, columnspan=4, pady=20)

        self.process_button = tk.Button(self.button_frame, text="Process", command=self.process_text, font=("Arial", 12), width=12)
        self.process_button.grid(row=0, column=0, padx=10)

        self.save_button = tk.Button(self.button_frame, text="Save", command=self.save_text, font=("Arial", 12), width=12)
        self.save_button.grid(row=0, column=1, padx=10)

        self.speak_button = tk.Button(self.button_frame, text="Speak", command=self.speak_text, font=("Arial", 12), width=12)
        self.speak_button.grid(row=0, column=2, padx=10)

        # Initialize Video Capture
        self.cap = cv2.VideoCapture(0)
        self.update_video_feed()

    def clear_textbox(self):
        self.text_box.delete("1.0", tk.END)

    def process_text(self):
        text = self.text_box.get("1.0", tk.END).strip()  # Get input text in Nepali script
        processed_text = []  # To store the processed text

        i = 0
        while i < len(text):
            current_char = text[i]

            # If the current character is a consonant and the next is a vowel
            if current_char in consonants_mapping.values():
                if i + 1 < len(text) and text[i + 1] in vowels_mapping.values():
                    consonant = list(consonants_mapping.keys())[list(consonants_mapping.values()).index(current_char)]
                    vowel = text[i + 1]

                    # Get the combined consonant-vowel from the matrix
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

        # Update the text box with the processed Nepali text
        self.text_box.delete("1.0", tk.END)
        self.text_box.insert("1.0", ''.join(processed_text))


    def save_text(self):
        self.process_text()
        text = self.text_box.get("1.0", tk.END).strip()

        if text:  # Check if there is any text to save
            current_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            filename = f"{current_time}_text.txt"

            with open(filename, "w", encoding="utf-8") as file:
                file.write(text)

            messagebox.showinfo("Save", f"Text saved successfully as {filename}!")
        else:
            messagebox.showwarning("Save", "No text to save!")

    def speak_text(self):
        self.process_text()  # Ensure processing is done before speaking
        text = self.text_box.get("1.0", tk.END).strip()

        if text:  # Check if there is text to speak
            try:
                # Generate speech using gTTS (Google Text-to-Speech)
                tts = gTTS(text, lang='ne')  # 'ne' is the language code for Nepali
                tts.save("temp.mp3")  # Save the generated speech as an audio file

                # Play the generated speech
                os.system("start temp.mp3")  # For Windows

                messagebox.showinfo("Speak", f"Speaking text: {text}")
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {e}")
        else:
            messagebox.showwarning("Speak", "No text to speak!")


    def update_video_feed(self):
        ret, frame = self.cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame)
            imgtk = ImageTk.PhotoImage(image=img)

            # Dynamically adjust video display to match the frame size
            self.video_display.imgtk = imgtk
            self.video_display.configure(image=imgtk)
        self.root.after(10, self.update_video_feed)

    def on_closing(self):
        self.cap.release()
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = SignAlphabetApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()
