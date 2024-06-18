from openai import OpenAI
from . import config

# new openai api client
openai_client = OpenAI(
    api_key=config.OPENAI_API_KEY
)

# generating question
def generate_questions(text):
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
    return questions
