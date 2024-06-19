from openai import OpenAI
from . import config
import sqlite3

# new openai api client
openai_client = OpenAI(
    api_key=config.OPENAI_API_KEY
)

# new db
def initialize_database():
    conn = sqlite3.connect('questions.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            key TEXT UNIQUE,
            value TEXT
        )
    ''')
    conn.commit()
    conn.close()

def print_all_questions():
    initialize_database()
    conn = sqlite3.connect('questions.db')
    cursor = conn.cursor()
    # Retrieve all rows from the database
    cursor.execute("SELECT * FROM questions")
    rows = cursor.fetchall()
    return rows


# generating question
def generate_questions(text):
    # db
    initialize_database()
    # connect db
    conn = sqlite3.connect('questions.db')
    cursor = conn.cursor()
    # Define your prompt for generating questions
    prompt = (
        f"Create a practice test with multiple choice questions on the following text:\n{text}\n\n"
        f"Each question should be on a different line. Each question should have 4 possible answers. "
        f"Under the possible answers, we should have the correct answer."
    )

    # Generate questions using the ChatGPT API
    response = openai_client.chat.completions.create(
        model='gpt-4o',
        messages=[
            {"role":"user", "content":prompt}
        ]
    )

    # Extract the generated questions from the API response
    questions = response.choices[0].message.content

    # Generate a unique key for the question
    base_key = ' '.join(text.split()[:2])
    key = base_key
    index = 1
    while key_exists(cursor, key):
        key = f"{base_key} {index}"
        index += 1

    # Insert the questions into the database
    value = questions
    cursor.execute("INSERT INTO questions (key, value) VALUES (?, ?)",(key, value))
    conn.commit()

    return questions

def key_exists(cursor, key):
    cursor.execute("SELECT COUNT(*) FROM questions WHERE key = ?", (key,))
    count = cursor.fetchone()[0]
    return count > 0
