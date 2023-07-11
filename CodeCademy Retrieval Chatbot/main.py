import json
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from gensim.models import Word2Vec
import backup_responses

# Loads JSON file
def load_json(file):
    try:
        with open(file) as bot_responses:
            print(f"Loaded '{file}' successfully.")
            return json.load(bot_responses)
    except FileNotFoundError:
        print(f"Error: File '{file}' not found.")
        return []

responses_data = load_json('bot_data.json')

if not responses_data:
    # Handle the case where the JSON file could not be loaded
    print("Error: No responses data available.")
    exit()

# Create a list of user inputs for vectorization
user_inputs = [response['user_input'] for response in responses_data]

# Flatten the user inputs
flattened_inputs = [item for sublist in user_inputs for item in sublist]

# Initialize and fit the TF-IDF vectorizer
tfidf_vectorizer = TfidfVectorizer()
tfidf_vectorizer.fit(flattened_inputs)

# Create Word2Vec model and train it on user inputs
word2vec_model = Word2Vec(sentences=user_inputs, min_count=1)

# Creates function to generate response
def get_response(input_string):
    split_message = re.split(r'\s+|[,;?!.-]\s*', input_string.lower())
    input_vector_tfidf = tfidf_vectorizer.transform([input_string.lower()])

    score_list = []

    for response in responses_data:
        response_score = 0
        required_score = 0
        required_words = response['required_words']

        if required_words:
            for word in split_message:
                if word in required_words:
                    required_score += 1

        if required_score == len(required_words):
            for word in split_message:
                if word in response["user_input"]:
                    response_score += 1

        score_list.append(response_score)

    best_response = max(score_list)

    if input_string.lower() == "exit":
        return "Goodbye! Thank you for chatting."

    if input_string == "":
        return "Please type a question so I may assist you."

    if best_response != 0:
        response_index = score_list.index(best_response)
        return responses_data[response_index]["bot_response"]

    return backup_responses.get_random_response()

while True:
    user_input = input("You: ")
    bot_response = get_response(user_input)
    print("Bot: ", bot_response)
    if bot_response.lower() == "goodbye! thank you for chatting.".lower():
        break

