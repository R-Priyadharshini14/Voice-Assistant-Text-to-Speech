from gtts import gTTS
import os
import speech_recognition as sr
from tkinter import *
from tkinter import messagebox
from datetime import datetime
from googletrans import Translator
import tkinter.ttk as ttk

# Initialize recognizer
recognizer = sr.Recognizer()

# Initialize translator
translator = Translator()

# Dictionary mapping language names to language codes
LANGUAGE_MAP = {
        "Albanian": "sq",
    "Amharic": "am",
    "Arabic": "ar",
    "Armenian": "hy",
    "Azerbaijani": "az",
    "Basque": "eu",
    "Belarusian": "be",
    "Bengali": "bn",
    "Bosnian": "bs",
    "Bulgarian": "bg",
    "Catalan": "ca",
    "Cebuano": "ceb",
    "Chichewa": "ny",
    "Chinese (Simplified)": "zh-CN",
    "Chinese (Traditional)": "zh-TW",
    "Corsican": "co",
    "Croatian": "hr",
    "Czech": "cs",
    "Danish": "da",
    "Dutch": "nl",
    "English": "en",
    "Esperanto": "eo",
    "Estonian": "et",
    "Filipino": "tl",
    "Finnish": "fi",
    "French": "fr",
    "Frisian": "fy",
    "Galician": "gl",
    "Georgian": "ka",
    "German": "de",
    "Greek": "el",
    "Gujarati": "gu",
    "Haitian Creole": "ht",
    "Hausa": "ha",
    "Hawaiian": "haw",
    "Hebrew": "iw",
    "Hindi": "hi",
    "Hmong": "hmn",
    "Hungarian": "hu",
    "Icelandic": "is",
    "Igbo": "ig",
    "Indonesian": "id",
    "Irish": "ga",
    "Italian": "it",
    "Japanese": "ja",
    "Javanese": "jw",
    "Kannada": "kn",
    "Kazakh": "kk",
    "Khmer": "km",
    "Kinyarwanda": "rw",
    "Korean": "ko",
    "Kurdish (Kurmanji)": "ku",
    "Kyrgyz": "ky",
    "Lao": "lo",
    "Latin": "la",
    "Latvian": "lv",
    "Lithuanian": "lt",
    "Luxembourgish": "lb",
    "Macedonian": "mk",
    "Malagasy": "mg",
    "Malay": "ms",
    "Malayalam": "ml",
    "Maltese": "mt",
    "Maori": "mi",
    "Marathi": "mr",
    "Mongolian": "mn",
    "Myanmar (Burmese)": "my",
    "Nepali": "ne",
    "Norwegian": "no",
    "Odia": "or",
    "Pashto": "ps",
    "Persian": "fa",
    "Polish": "pl",
    "Portuguese": "pt",
    "Punjabi": "pa",
    "Romanian": "ro",
    "Russian": "ru",
    "Samoan": "sm",
    "Scots Gaelic": "gd",
    "Serbian": "sr",
    "Sesotho": "st",
    "Shona": "sn",
    "Sindhi": "sd",
    "Sinhala": "si",
    "Slovak": "sk",
    "Slovenian": "sl",
    "Somali": "so",
    "Spanish": "es",
    "Sundanese": "su",
    "Swahili": "sw",
    "Swedish": "sv",
    "Tajik": "tg",
    "Tamil": "ta",
    "Telugu": "te",
    "Thai": "th",
    "Turkish": "tr",
    "Ukrainian": "uk",
    "Urdu": "ur",
    "Uyghur": "ug",
    "Uzbek": "uz",
    "Vietnamese": "vi",
    "Welsh": "cy",
    "Xhosa": "xh",
    "Yiddish": "yi",
    "Yoruba": "yo",
    "Zulu": "zu"
}

# Function to convert text to speech
def text_to_speech():
    # Read inputs given by user
    text = text_entry1.get("1.0", "end-1c")
    translate_to_language = translate_combo.get()

    # Check if the user submitted inputs
    if len(text.strip()) == 0:
        messagebox.showerror(message="Enter text to convert to speech")
        return

    # Get language code for translation
    translate_to_language_code = LANGUAGE_MAP.get(translate_to_language)

    # Translate text if translation language is selected
    if translate_to_language_code:
        translated_text = translator.translate(text, dest=translate_to_language_code)
        text = translated_text.text

    # Convert the text to speech
    speech = gTTS(text=text, lang=translate_to_language_code, slow=False)

    # Save the speech to an MP3 file
    speech.save("text.mp3")

    # Play the file
    os.system("mpg123 " + "text.mp3")

# Function to capture audio from microphone and transcribe
# Function to capture audio from microphone and transcribe
def speech_to_text():
    try:
        # Capture audio from the microphone
        with sr.Microphone() as source:
            print("Speak something...")
            audio = recognizer.listen(source)

        # Transcribe audio using Google Speech Recognition
        transcription = recognizer.recognize_google(audio)

        # Get the selected language for translation
        translate_to_language = translate_combo.get()
        translate_to_language_code = LANGUAGE_MAP.get(translate_to_language)

        # Translate the transcription to the selected language
        if translate_to_language_code:
            translated_text = translator.translate(transcription, dest=translate_to_language_code)
            transcription = translated_text.text

        # Append current date and time to the transcription
        current_time = datetime.now().strftime("%d/%m/%Y %I:%M%p")
        transcription_with_time = f"{transcription}\t{current_time}\n"

        # Display the transcription in text entry field
        text_entry2.delete("1.0", "end")
        text_entry2.insert("1.0", transcription_with_time)
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
        messagebox.showerror(message="Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
        messagebox.showerror(message="Could not request results from Google Speech Recognition service; {0}".format(e))

def clear_text():
    text_entry1.delete("1.0", "end")
   
# Function to save transcription to a file
def save_transcription():
    transcription = text_entry1.get("1.0", "end-1c")
    transcription = text_entry2.get("1.0", "end-1c")

    if len(transcription.strip()) == 0:
        messagebox.showerror(message="No transcription to save")
        return

    # Append the transcription along with date and time to the file
    current_time = datetime.now().strftime("%d/%m/%Y %I:%M%p")
    transcription_with_time = f"{transcription}\t{current_time}\n"
    with open("transcription.txt", "a", encoding="utf-8") as file:

        file.write(transcription_with_time)

    messagebox.showinfo(message="Transcription saved successfully")


# Function to translate text to selected language
# Function to translate text to selected language
def translate_text():
    # Get the text to translate from the first text box
    original_text = text_entry1.get("1.0", "end-1c")
    if len(original_text.strip()) == 0:
        messagebox.showerror(message="Enter text to translate")
        return

    # Get the selected language
    selected_language = LANGUAGE_MAP[translate_combo.get()]

    # Translate the text
    translated_text = translator.translate(original_text, dest=selected_language)

    # Display the translated text in the second text entry field
    text_entry2.delete("1.0", "end")
    text_entry2.insert("1.0", translated_text.text)

    # Re-insert the original text into the first text entry field
    text_entry1.delete("1.0", "end")
    text_entry1.insert("1.0", original_text)

# Function to change the theme
def change_theme():
    # Get the current background color
    current_color = window.cget("bg")

    # List of available colors
    colors = ["green", "skyblue", "lightgreen", "lightblue", "pink", "yellow", "purple"]

    try:
        # Find the index of the current color
        index = colors.index(current_color)
    except ValueError:
        # Use white color if current color is not in the list
        index = -1

    # Calculate the index of the next color
    next_index = (index + 1) % len(colors)

    # Change the background color to the next color
    window.configure(bg=colors[next_index])

# Function to create the second page
def create_second_page():
    # Destroy the widgets of the front page
    button_front_page.destroy()

    # Show the widgets of the second page
    text_label1.grid(row=0, column=0, padx=10, pady=10)
    text_entry1.grid(row=0, column=1, padx=10, pady=10)
    text_label2.grid(row=1, column=0, padx=10, pady=10)
    text_entry2.grid(row=1, column=1, padx=10, pady=10)
    translate_label.grid(row=2, column=0, padx=10, pady=10)
    translate_combo.grid(row=2, column=1, padx=10, pady=10)
    button_text_to_speech.grid(row=3, column=0, padx=10, pady=10)
    button_speech_to_text.grid(row=3, column=1, padx=10, pady=10)
    button_clear_text.grid(row=4, column=0, padx=10, pady=10)
    button_save_transcription.grid(row=4, column=1, padx=10, pady=10)
    button_translate.grid(row=5, column=0, padx=10, pady=10)
    button_change_theme.grid(row=5, column=1, padx=10, pady=10)
    button_exit.grid(row=6, column=0, columnspan=2, pady=20)

# GUI setup
window = Tk()
window.geometry("700x400")
window.title("Voice Assistant: Text and Speech Processing Tool")
window.configure(bg='lightgrey')

# Front page button
button_front_page = Button(window, text='Voice Assistant: Text and Speech Processing Tool', command=create_second_page, bg='blue', fg='white', font=("Arial", 14))
button_front_page.place(relx=0.5, rely=0.5, anchor=CENTER)

# Text entry field and Combo boxes (Second page widgets)
text_label1 = Label(window, text="Text:", font=("Arial", 14))
text_entry1 = Text(window, width=50, height=5, font=("Arial", 12))
text_label2 = Label(window, text="Translation:", font=("Arial", 14))
text_entry2 = Text(window, width=50, height=5, font=("Arial", 12))
translate_label = Label(window, text="Translate to:", font=("Arial", 14))
translate_combo = ttk.Combobox(window, values=list(LANGUAGE_MAP.keys()), font=("Arial", 12))
translate_combo.current(0)

# Buttons (Second page widgets)
button_text_to_speech = Button(window, text='Convert Text to Speech', bg='Turquoise', fg='Red', command=text_to_speech, font=("Arial", 12))
button_speech_to_text = Button(window, text='Convert Speech to Text', bg='Turquoise', fg='Red', command=speech_to_text, font=("Arial", 12))
button_clear_text = Button(window, text='Clear Text', bg='Turquoise', fg='Red', command=clear_text, font=("Arial", 12))
button_save_transcription = Button(window, text='Save Transcription', bg='Turquoise', fg='Red', command=save_transcription, font=("Arial", 12))
button_translate = Button(window, text='Translate Text', bg='Turquoise', fg='Red', command=translate_text, font=("Arial", 12))
button_change_theme = Button(window, text='Theme', bg='Turquoise', fg='Red', command=change_theme, font=("Arial", 12))
button_exit = Button(window, text='Exit', bg='Turquoise', fg='Red', command=window.destroy, font=("Arial", 12))

# Start GUI event loop
window.mainloop()
