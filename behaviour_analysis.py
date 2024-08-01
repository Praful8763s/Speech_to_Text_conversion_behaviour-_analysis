import pandas as pd
import mysql.connector
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

# Sample data (in a real scenario, this should be replaced with actual data)
db = mysql.connector.connect(
    host="localhost",
    user="yourusername",
    password="yourpassword",
    database="PrisonerDatabase"
)
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

# Function to predict release recommendation
def predict_release(age, sentence_length, education_level, behavior_score):
    input_data = pd.DataFrame([[age, sentence_length, education_level, behavior_score]],
                              columns=['age', 'sentence_length', 'education_level', 'behavior_score'])
    prediction = model.predict(input_data)
    return "Release" if prediction[0] == 1 else "Do not release"

# Example usage
age = 30
sentence_length = 6
education_level = 2
behavior_score = 7

recommendation = predict_release(age, sentence_length, education_level, behavior_score)
print(f"Recommendation: {recommendation}")
