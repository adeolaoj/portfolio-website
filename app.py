from flask import Flask, request, jsonify, render_template
import tensorflow as tf
import numpy as np
import nltk
nltk.download('punkt')
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
import pickle
import json
import random

app = Flask(__name__)

# Load model and metadata
model = tf.keras.models.load_model("chatbot_model.keras")
with open('metadata.pkl', 'rb') as file:
    data = pickle.load(file)
    word_stems = data['words']
    classes = data['classes']

with open('intents.json') as file:
    intents = json.load(file)

ps = PorterStemmer()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json['message']
    tokens = word_tokenize(user_input)
    processed_tokens = []

    for token in tokens:
        lower = token.lower()
        stem = ps.stem(lower)
        processed_tokens.append(stem)

    bow_vector = [0] * len(word_stems)
    
    for token in processed_tokens:
        if token in word_stems:
            bow_vector[word_stems.index(token)] = 1

    bow_vector = np.array(bow_vector).reshape(1, -1)

    output = model.predict(bow_vector)[0]

    prediction_index = np.argmax(output)
    intent = classes[prediction_index]
    confidence = output[prediction_index]

    if confidence <= 0.3:  # catch unrelated messages
        intent = "fallback"

    if intent != "fallback":
        for intent_tag in intents['intents']:
            if intent_tag['tag'] == intent:
                response = random.choice(intent_tag['responses'])
    else:
        response = "Hmm, I can't answer that right now... buttt I can tell you about my skills or projects!"

    print("Confidence: ", confidence)
    return jsonify({'response': response})
    


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)

