import tensorflow as tf
import nltk
nltk.download('punkt')
nltk.download('punkt_tab')
import numpy as np
from tensorflow.keras.models import Sequential # type: ignore
from tensorflow.keras.layers import Dense # type: ignore
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
import pickle
import random
import json

# load the trained model
model = tf.keras.models.load_model("chatbot_model.keras")

# load the metadata
with open('metadata.pkl', 'rb') as file:
    data = pickle.load(file)
    word_stems = data['words']
    classes = data['classes']

with open('intents.json') as file:
    intents = json.load(file)

ps = PorterStemmer()

# collect user input and formulate a response
user_tokens = []

while True:
    user_input = input("You: ")
    if (user_input.lower() == "quit"): # break if user enters quit
        break

    # separate user input into tokens
    user_tokens = word_tokenize(user_input)
    processed_tokens = []

    # preprocess tokens (stem, lower)
    for token in user_tokens:
        lower = token.lower()
        stem = ps.stem(lower)
        processed_tokens.append(stem)

    # create bag of words vector
    bow_vector = [0] * len(word_stems)

    for token in processed_tokens:
        if token in word_stems:
            bow_vector[word_stems.index(token)] = 1

    bow_vector = np.array(bow_vector).reshape(1, -1) #convert vector to numpy array

    # predict the intent of the user input using the model
    output = model.predict(bow_vector)[0]

    # find the intent with the highest probability
    prediction_index = np.argmax(output) # index of highest probable intent
    intent = classes[prediction_index] # tag associated with intent
    confidence = output[prediction_index]

    if confidence <= 0.2:  # catch unrelated messages
        intent = "fallback"

    if intent != "fallback":
        for intent_tag in intents['intents']:
            if intent_tag['tag'] == intent:
                response = random.choice(intent_tag['responses'])
                print("Bot: ", response)
    else:
        print("Bot: Hmm, I can't answer that right now... buttt I can tell you about my skills or projects!")



    


