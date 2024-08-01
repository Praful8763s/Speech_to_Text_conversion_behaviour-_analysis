import speech_recognition as sr
from googletrans import Translator, LANGUAGES

def recognize_speech_from_mic(recognizer, microphone, language_code):
    """Transcribe speech from recorded from `microphone`."""
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        print("Say something...")
        audio = recognizer.listen(source)

    response = {
        "success": True,
        "error": None,
        "transcription": None
    }

    try:
        response["transcription"] = recognizer.recognize_google(audio, language=language_code)
    except sr.RequestError:
        response["success"] = False
        response["error"] = "API unavailable"
    except sr.UnknownValueError:
        response["error"] = "Unable to recognize speech"

    return response

def main():
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    languages = {
        "1": "mr-IN",  # Marathi
        "2": "hi-IN",  # Hindi
        "3": "en-IN",  # English
        "4": "bn-IN",  # Bengali
        "5": "gu-IN",  # Gujarati
        "6": "as-IN",  # Assamese
        "7": "pa-IN",  # Punjabi
        "8": "te-IN",  # Telugu
        "9": "ml-IN",  # Malayalam
        "10": "ur-IN"  # Urdu (closest to Uttarkhand language)
    }

    print("Select a language:")
    for key, value in LANGUAGES.items():
        print(f"{key}: {value}")

    language_choice = input("Enter the number corresponding to your language: ")

    if language_choice not in languages:
        print("Invalid choice")
        return

    language_code = languages[language_choice]

    print(f"You selected {LANGUAGES[language_code]}")

    response = recognize_speech_from_mic(recognizer, microphone, language_code)

    if response["success"]:
        print("You said: {}".format(response["transcription"]))
    else:
        print("I didn't catch that. What did you say?\nError: {}".format(response["error"]))

if __name__ == "__main__":
    main()
