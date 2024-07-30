import customtkinter as ctk
import os
from gtts import gTTS
from tkinter import filedialog, Tk
from CTkListbox import CTkListbox
from CTkMessagebox import CTkMessagebox

# Set the appearance and theme of the application
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# Language options for TTS
LANGUAGES = {
    'af': 'Afrikaans', 'ar': 'Arabic', 'bg': 'Bulgarian', 'bn': 'Bengali', 'bs': 'Bosnian',
    'ca': 'Catalan', 'cs': 'Czech', 'da': 'Danish', 'de': 'German', 'el': 'Greek', 'en': 'English',
    'es': 'Spanish', 'et': 'Estonian', 'fi': 'Finnish', 'fr': 'French', 'gu': 'Gujarati', 'hi': 'Hindi',
    'hr': 'Croatian', 'hu': 'Hungarian', 'id': 'Indonesian', 'is': 'Icelandic', 'it': 'Italian', 'iw': 'Hebrew',
    'ja': 'Japanese', 'jw': 'Javanese', 'km': 'Khmer', 'kn': 'Kannada', 'ko': 'Korean', 'la': 'Latin',
    'lv': 'Latvian', 'ml': 'Malayalam', 'mr': 'Marathi', 'ms': 'Malay', 'my': 'Myanmar (Burmese)',
    'ne': 'Nepali', 'nl': 'Dutch', 'no': 'Norwegian', 'pl': 'Polish', 'pt': 'Portuguese',
    'ro': 'Romanian', 'ru': 'Russian', 'si': 'Sinhala', 'sk': 'Slovak', 'sq': 'Albanian', 'sr': 'Serbian',
    'su': 'Sundanese', 'sv': 'Swedish', 'sw': 'Swahili', 'ta': 'Tamil', 'te': 'Telugu', 'th': 'Thai',
    'tl': 'Filipino', 'tr': 'Turkish', 'uk': 'Ukrainian', 'ur': 'Urdu', 'vi': 'Vietnamese',
    'zh-CN': 'Chinese (Simplified)',
    'zh-TW': 'Chinese (Mandarin/Taiwan)', 'zh': 'Chinese (Mandarin)'
}


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Set up the main window properties
        self.title("Text To Speech")
        self.geometry("1200x200")
        self.minsize(1200, 150)
        self.maxsize(1600, 300)

        self.speech_counter = 0

        # Initialize the UI components
        self._initialize_components()

    def _initialize_components(self):
        # Text box for user's text entry
        self.text_box = ctk.CTkTextbox(self, corner_radius=15)
        self.text_box.place(relx=0.28, rely=0.01, relwidth=0.4, relheight=0.95)
        self.text_box.insert("0.0", "Your text here")

        # Check box for choosing slow or default speech
        self.slowed_var = ctk.StringVar(value="off")
        self.slowed_checkbox = ctk.CTkCheckBox(self, text="Slow speech: Off", command=self.update_slowed_text,
                                               variable=self.slowed_var, onvalue="on", offvalue="off")
        self.slowed_checkbox.place(relx=0.01, rely=0.15)

        # Label for show current language
        self.selected_language_label = ctk.CTkLabel(self, text="Choosed language for TTS: Afrikaans",
                                                    fg_color="transparent", font=ctk.CTkFont(family="Arial", size=12))
        self.selected_language_label.place(relx=0.01, rely=0.8)

        # Option menu for choosing language of speech
        self.language_menu = CTkListbox(self, command=self.update_language_text)
        self.language_menu.place(relx=0.01, rely=0.4, relheight=0.4)

        for i in list(LANGUAGES.keys()):
            self.language_menu.insert("end", i)
        self.language_menu.activate(0)

        # Option menu for choosing language of speech
        self.activate_tts_button = ctk.CTkButton(self, text="Activate and save TTS",
                                                 corner_radius=15, command=self.activate_tts)
        self.activate_tts_button.place(relx=0.79, rely=0.4)

        # Check box for choosing will be speech played after save or not
        self.play_var = ctk.StringVar(value="off")
        self.play_checkbox = ctk.CTkCheckBox(self, text="Play after save: Off", command=self.update_play_text,
                                             variable=self.play_var, onvalue="on", offvalue="off")
        self.play_checkbox.place(relx=0.795, rely=0.625)

    def activate_tts(self):
        # Getting all settings for tts
        text = self.text_box.get("0.0", "end").strip()
        language = self.language_menu.get()
        slow = self.slowed_var.get() == "on"

        # Check if text is empty, if empty then function will stop
        if not text:
            CTkMessagebox(title="Activating TTS (Error)", message="Text is empty",
                          icon="cancel", option_1="Ok", sound=True)
            return

        # Creating speech
        speech = gTTS(text=text, lang=language, slow=slow)

        # Trying to ask directory for saving and playing generated speech
        try:
            root = Tk(); root.withdraw()
            file_path = filedialog.askdirectory(title="Choose a directory for saving speech")
            if file_path:
                self.speech_counter += 1
                full_path = os.path.join(file_path, f'speech{self.speech_counter}.mp3')
                speech.save(full_path)
                if self.play_var.get() == "on":
                    os.system(full_path)
                root.destroy()
            else:
                CTkMessagebox(title="Saving TTS (not saved)", message="Please choose a directory for saving",
                              icon="cancel", option_1="Ok", sound=True)
                root.destroy()
        except Exception as error:
            CTkMessagebox(title="Saving TTS (not saved)", message=f"Unexpected error while saving: {error}",
                          icon="cancel", option_1="Ok", sound=True)

    def update_language_text(self, lang):
        if lang in LANGUAGES:
            self.selected_language_label.configure(text=f"Choosed language for TTS: {LANGUAGES[lang]}")
        else:
            self.selected_language_label.configure(text="Invalid language selected")

    def update_slowed_text(self):
        self.slowed_checkbox.configure(text=f"Slow speech: {self.slowed_var.get().title()}")

    def update_play_text(self):
        self.play_checkbox.configure(text=f"Play after save: {self.play_var.get().title()}")

if __name__ == '__main__':
    app = App()
    app.mainloop()
