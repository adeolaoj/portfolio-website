import json
import numpy as np
import nltk
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
nltk.download('punkt')
nltk.download('punkt_tab')
import tensorflow as tf
from tensorflow.keras.models import Sequential # type: ignore
from tensorflow.keras.layers import Dense # type: ignore
import pickle


ps = PorterStemmer()

'''
Preprocessing the data from the json file
'''

with open('intents.json') as file:
    data = json.load(file)



words = [] # list of words
classes = [] # intent tags
documents = [] # list of all (processed pattern, intent tag) pairs (tokens and associated tags)
word_stems = [] # all unique stemmed+lowercase words (model vocabulary)

for intent in data['intents']:
    for pattern in intent['patterns']:
        tokens = word_tokenize(pattern) # grab the individual words from the list of patterns
        processed_tokens = []
        
        for token in tokens: # process the words (tokens) by taking them to lowercase and stripping them down to their stems
            lower = token.lower()
            stem = ps.stem(lower)
            processed_tokens.append(stem) # add the processed words to a list
            if stem not in word_stems:
                word_stems.append(stem) # add non-duplicate word stems to a list

        words.extend(processed_tokens) # add the processed tokens to a list

        documents.append((processed_tokens, intent['tag']))

        if intent['tag'] not in classes:
            classes.append(intent['tag'])

word_stems = sorted(set(word_stems))
classes = sorted(set(classes))

'''
Creating the bag-of-words vector
'''

training_data = []  # will store tuples containing bag of words vector and encoded labels

for processed_token, intent in documents:
    bow_vector = [0] * len(word_stems)
    for token in processed_token:
        if token in word_stems:
            bow_vector[word_stems.index(token)] = 1

    label_vector = [0] * len(classes) # intent labels
    label_index = classes.index(intent) # label index
    label_vector[label_index] = 1 # one-hot encoding the labels

    training_data.append((bow_vector, label_vector))

X = np.array([item[0] for item in training_data])
y = np.array([item[1] for item in training_data])


'''
Creating a sequential model for the chatbot
'''

model = Sequential()

model.add((tf.keras.layers.Dense(units=4, activation='relu', input_shape=(len(word_stems),)))) # input layer
model.add(tf.keras.layers.Dense(units=4, activation='relu')) #hidden layer
model.add(tf.keras.layers.Dense(units=len(y[0]), activation='softmax')) #output layer

# compilation of model
model.compile(
    loss='categorical_crossentropy',  # calculate loss by comparing actual label and probability distribution
    optimizer='adam',
    metrics=['accuracy']
)

# training the model
model.fit(X, y, epochs=110, batch_size=4, verbose=1)

model.save("chatbot_model.keras") # save output
pickle.dump({'words': word_stems, 'classes': classes}, open("metadata.pkl", "wb"))


