import random

# Function that provides list of responses for when question asked does not pull up an answer
def get_random_response():
    random_list = [
        "I'm sorry, can you rephrase the question?",
        "I'm sorry, please retype your response.",
        "I'm sorry, can you word your question a bit differently?",
        "You've asked a great question that unfortunately I cannot understand. Can you reword it?",
        "Would you mind rephrasing the question for me, thank you!"
    ]

    list_count = len(random_list)
    random_item = random.randrange(list_count)

    return random_list[random_item]