import tkinter as tk
from tkinter import filedialog, messagebox
from gtts import gTTS  # Google Text-to-Speech for Nepali support
import os

class NepaliSignLanguageApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Nepali Sign Language to Text")
        self.sentence = ""  # To store the recognized sentence in Nepali

        # Main Frame
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(pady=20, padx=20)

        # Text display
        self.sentence_label = tk.Label(self.main_frame, text="Recognized Sentence:", font=("Arial", 14))
        self.sentence_label.grid(row=0, column=0, sticky="w", pady=10)

        self.sentence_display = tk.Label(self.main_frame, text="", font=("Arial", 16), fg="blue", wraplength=400, anchor="w")
        self.sentence_display.grid(row=1, column=0, sticky="w", pady=10)

        # Buttons
        self.save_button = tk.Button(self.main_frame, text="Save Sentence", font=("Arial", 12), command=self.save_sentence)
        self.save_button.grid(row=2, column=0, sticky="w", pady=10)

        self.clear_button = tk.Button(self.main_frame, text="Clear Sentence", font=("Arial", 12), command=self.clear_sentence)
        self.clear_button.grid(row=2, column=1, sticky="e", pady=10)

        # Key bindings (Simulated letter detection for Nepali testing)
        self.root.bind("<KeyPress>", self.key_press_simulation)

    def key_press_simulation(self, event):
        """
        Simulates letter recognition for testing. Adds Nepali letters to the sentence when keys are pressed.
        """
        # Add the character if it's a Devanagari script letter
        if "\u0900" <= event.char <= "\u097F":  # Unicode range for Devanagari
            self.sentence += event.char
            self.update_sentence_display()

    def update_sentence_display(self):
        """Updates the sentence display on the interface."""
        self.sentence_display.config(text=self.sentence)

    def save_sentence(self):
        """Saves the recognized sentence to a text file and converts it to speech."""
        if not self.sentence.strip():
            messagebox.showwarning("Warning", "No sentence to save!")
            return

        # Save sentence to a text file
        file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                                 filetypes=[("Text Files", "*.txt")],
                                                 title="Save Sentence")
        if file_path:
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(self.sentence)
            messagebox.showinfo("Info", f"Sentence saved to {file_path}")

            # Convert to Nepali speech
            self.convert_to_speech()

    def convert_to_speech(self):
        """Converts the sentence to Nepali speech using gTTS."""
        try:
            tts = gTTS(text=self.sentence, lang="ne")
            audio_path = "output.mp3"
            tts.save(audio_path)
            os.system(f"start {audio_path}")  # Use appropriate command based on your OS
        except Exception as e:
            messagebox.showerror("Error", f"Failed to convert to speech: {str(e)}")

    def clear_sentence(self):
        """Clears the current recognized sentence."""
        self.sentence = ""
        self.update_sentence_display()

# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = NepaliSignLanguageApp(root)
    root.mainloop()
