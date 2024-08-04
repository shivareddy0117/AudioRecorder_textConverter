import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Embedding, Bidirectional
from tensorflow.keras.optimizers import Adam
import numpy as np

# Sample data: List of sentences
data = [
    "Hello how are you",
    "What is your name",
    "Where do you live",
    "How old are you",
    "What are you doing",
    "I am reading a book",
    "I am playing a game"
]

# Preparing the Tokenizer and fitting on the text data
tokenizer = Tokenizer()
tokenizer.fit_on_texts(data)

# Vocabulary size
vocab_size = len(tokenizer.word_index) + 1

# Generating sequences of tokens
input_sequences = []
for line in data:
    token_list = tokenizer.texts_to_sequences([line])[0]
    for i in range(1, len(token_list)):
        n_gram_sequence = token_list[:i+1]
        input_sequences.append(n_gram_sequence)

# Padding sequences
max_sequence_len = max(len(x) for x in input_sequences)
input_sequences = np.array(pad_sequences(input_sequences, maxlen=max_sequence_len, padding='pre'))

# Creating predictors and label
xs, labels = input_sequences[:,:-1], input_sequences[:,-1]
ys = tf.keras.utils.to_categorical(labels, num_classes=vocab_size)

# Model definition
model = Sequential([
    Embedding(vocab_size, 64, input_length=max_sequence_len-1),
    Bidirectional(LSTM(20)),
    Dense(vocab_size, activation='softmax')
])

# Compiling the model
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
print(model.summary())

# Training the model
model.fit(xs, ys, epochs=100, verbose=1)

# Function to predict the next word
def predict_next_word(text):
    sequence = tokenizer.texts_to_sequences([text])[0]
    padded_sequence = pad_sequences([sequence], maxlen=max_sequence_len-1, padding='pre')
    prediction = model.predict(padded_sequence)
    predicted_word_index = np.argmax(prediction)
    predicted_word = tokenizer.index_word[predicted_word_index]
    return predicted_word

# Testing the prediction
print(predict_next_word("What are you"))
