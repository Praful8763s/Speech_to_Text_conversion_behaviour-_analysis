import speech_recognition as sr
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
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

def behavior_analysis_model():
    # Sample data (in a real scenario, this should be replaced with actual data)
    data = {
        'age': [25, 45, 35, 50, 23, 34, 44, 22, 39, 48],
        'sentence_length': [5, 10, 7, 15, 3, 6, 9, 2, 8, 12],
        'education_level': [3, 2, 1, 2, 3, 1, 2, 3, 1, 2],
        'behavior_score': [8, 5, 6, 4, 9, 7, 5, 10, 6, 3],
        'release_recommendation': [1, 0, 1, 0, 1, 1, 0, 1, 1, 0]
    }

    # Create a DataFrame
    df = pd.DataFrame(data)

    # Features and target variable
    X = df[['age', 'sentence_length', 'education_level', 'behavior_score']]
    y = df['release_recommendation']

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Initialize the model
    model = RandomForestClassifier(n_estimators=100, random_state=42)

    # Train the model
    model.fit(X_train, y_train)

    # Make predictions
    y_pred = model.predict(X_test)

    # Evaluate the model
    accuracy = accuracy_score(y_test, y_pred)
    report = classification_report(y_test, y_pred)

    print(f"Accuracy: {accuracy}")
    print("Classification Report:")
    print(report)

    return model

def predict_release(model, age, sentence_length, education_level, behavior_score):
    input_data = pd.DataFrame([[age, sentence_length, education_level, behavior_score]],
                              columns=['age', 'sentence_length', 'education_level', 'behavior_score'])
    prediction = model.predict(input_data)
    return "Release" if prediction[0] == 1 else "Do not release"

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
    for key, value in languages.items():
        print(f"{key}: {LANGUAGES[value.split('-')[0]]}")

    language_choice = input("Enter the number corresponding to your language: ")

    if language_choice not in languages:
        print("Invalid choice")
        return

    language_code = languages[language_choice]

    print(f"You selected {LANGUAGES[language_code.split('-')[0]]}")

    response = recognize_speech_from_mic(recognizer, microphone, language_code)

    if response["success"]:
        print("You said: {}".format(response["transcription"]))
    else:
        print("I didn't catch that. What did you say?\nError: {}".format(response["error"]))

    model = behavior_analysis_model()

    # Example usage
    age = 30
    sentence_length = 6
    education_level = 2
    behavior_score = 7

    recommendation = predict_release(model, age, sentence_length, education_level, behavior_score)
    print(f"Recommendation: {recommendation}")

if __name__ == "__main__":
    main()
