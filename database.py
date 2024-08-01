import mysql.connector
from faker import Faker
import random

# Establish database connection
db = mysql.connector.connect(
    host="localhost",
    user="yourusername",
    password="yourpassword",
    database="PrisonerDatabase"
)

cursor = db.cursor()

# Initialize Faker for generating random data
faker = Faker()

# Generate and insert data
for _ in range(10000000):  # 1 crore = 10 million
    name = faker.name()
    age = random.randint(18, 80)
    sentence_length = random.randint(1, 20)
    education_level = random.randint(0, 3)
    behavior_score = random.randint(1, 10)
    release_recommendation = random.choice([0, 1])
    language_code = random.choice(['mr-IN', 'hi-IN', 'en-IN', 'bn-IN', 'gu-IN', 'as-IN', 'pa-IN', 'te-IN', 'ml-IN', 'ur-IN'])
    
    cursor.execute("""
        INSERT INTO Prisoners (name, age, sentence_length, education_level, behavior_score, release_recommendation, language_code)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (name, age, sentence_length, education_level, behavior_score, release_recommendation, language_code))

    if _ % 10000 == 0:
        db.commit()
        print(f'Inserted {_} records')

db.commit()
cursor.close()
db.close()
