import pickle
import json
import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Activation, Dropout
from keras.optimizers import SGD
import random

import nltk

nltk.download('punkt')
nltk.download('wordnet')


from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()


try:
    with open("words.pkl", "rd") as fle:
        words = pickle.load(fle)

    with open("classes.pkl", "rd") as fle:
        classes = pickle.load(fle)

except:
    words = []
    classes = []
    documents = []
    ignore_letters = ['!', '?', ',', '.', '(', ')']
    intents_file = open('static/its.json').read()
    intents = json.loads(intents_file)

    for intent in intents['intents']:
        for pattern in intent['patterns']:
            word = nltk.word_tokenize(pattern)
            words.extend(word)
            documents.append((word, intent['tag']))
        if intent['tag'] not in classes:
            classes.append(intent['tag'])

    words = [lemmatizer.lemmatize(w.lower()) for w in words if w not in ignore_letters]
    words = sorted(list(set(words)))
    classes = sorted(list(set(classes)))

    pickle.dump(words, open('words.pkl', 'wb'))
    pickle.dump(classes, open('classes.pkl', 'wb'))

    training = []
    output_empty = [0] * len(classes)
    for doc in documents:
        bag = []
        pattern_words = doc[0]
        pattern_words = [lemmatizer.lemmatize(word.lower()) for word in pattern_words]
        for word in words:
            bag.append(1) if word in pattern_words else bag.append(0)

        output_row = list(output_empty)
        output_row[classes.index(doc[1])] = 1

        training.append([bag, output_row])

    training = np.array(training)
    train_x = list(training[:, 0])
    train_y = list(training[:, 1])
    print("Training data created")


# Create model - 3 layers. First layer 128 neurons, second layer 64 neurons and 3rd output layer contains number of neurons
# equal to number of intents to predict output intent with softmax
model = Sequential()
model.add(Dense(128, input_shape=(len(train_x[0]),), activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(64, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(len(train_y[0]), activation='softmax'))

sgd = SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])

try:
    model.load('content/chatbot_model.h5')
except:
    hist = model.fit(np.array(train_x), np.array(train_y), epochs=800, batch_size=8)
    model.save('content/chatbot_model.h5', hist)

print("model created")
