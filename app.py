from flask import Flask, request, render_template, jsonify
import speech_recognition as sr
import pandas as pd
from sklearn.ensemble import RandomForestClassifier

app = Flask(__name__)

# Behavior Analysis Model
def train_behavior_model():
    data = {
        'age': [25, 45, 35, 50, 23, 34, 44, 22, 39, 48],
        'sentence_length': [5, 10, 7, 15, 3, 6, 9, 2, 8, 12],
        'education_level': [3, 2, 1, 2, 3, 1, 2, 3, 1, 2],
        'behavior_score': [8, 5, 6, 4, 9, 7, 5, 10, 6, 3],
        'release_recommendation': [1, 0, 1, 0, 1, 1, 0, 1, 1, 0]
    }
    df = pd.DataFrame(data)
    X = df[['age', 'sentence_length', 'education_level', 'behavior_score']]
    y = df['release_recommendation']
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X, y)
    return model

model = train_behavior_model()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/speech-to-text', methods=['POST'])
def speech_to_text():
    recognizer = sr.Recognizer()
    audio_file = request.files['audio']
    language_code = request.form['language']

    with sr.AudioFile(audio_file) as source:
        audio = recognizer.record(source)
    
    try:
        text = recognizer.recognize_google(audio, language=language_code)
        return jsonify({'success': True, 'transcription': text})
    except sr.UnknownValueError:
        return jsonify({'success': False, 'error': 'Unable to recognize speech'})
    except sr.RequestError:
        return jsonify({'success': False, 'error': 'API unavailable'})

@app.route('/behavior-analysis', methods=['POST'])
def behavior_analysis():
    data = request.json
    input_data = pd.DataFrame([data], columns=['age', 'sentence_length', 'education_level', 'behavior_score'])
    prediction = model.predict(input_data)
    result = "Release" if prediction[0] == 1 else "Do not release"
    return jsonify({'recommendation': result})

if __name__ == '__main__':
    app.run(debug=True)
