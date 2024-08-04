import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Embedding, Bidirectional
from tensorflow.keras.optimizers import Adam
import numpy as np
import os

# Function to load data from a directory and save to a single file
def load_data_from_directory(directory, output_file):
    sentences = []
    with open(output_file, 'w', encoding='utf-8') as outfile:
        for filename in os.listdir(directory):
            if filename.endswith(".txt"):
                file_path = os.path.join(directory, filename)
                with open(file_path, 'r', encoding='utf-8') as file:
                    sentence = file.read().strip()
                    sentences.append(sentence)
                    outfile.write(sentence + '\n')
    return sentences

# Directory containing the text files and output file path
directory = r'C:\Users\SAHITHYAMOGILI\Desktop\Projects\AudioToText\text_dir'  # Update this path accordingly
output_file = 'combined_sentences.txt'  # Path for the output text file
data = load_data_from_directory(directory, output_file)

# # Continue with your existing tokenizer, sequence generation, and padding steps
# tokenizer = Tokenizer()
# tokenizer.fit_on_texts(data)

# vocab_size = len(tokenizer.word_index) + 1

# input_sequences = []
# for line in data:
#     token_list = tokenizer.texts_to_sequences([line])[0]
#     for i in range(1, len(token_list)):
#         n_gram_sequence = token_list[:i+1]
#         input_sequences.append(n_gram_sequence)

# max_sequence_len = max(len(x) for x in input_sequences)
# input_sequences = np.array(pad_sequences(input_sequences, maxlen=max_sequence_len, padding='pre'))

# xs, labels = input_sequences[:,:-1], input_sequences[:,-1]
# ys = tf.keras.utils.to_categorical(labels, num_classes=vocab_size)

# # Model and training
# model = Sequential([
#     Embedding(vocab_size, 64, input_length=max_sequence_len-1),
#     Bidirectional(LSTM(20)),
#     Dense(vocab_size, activation='softmax')
# ])

# model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
# model.fit(xs, ys, epochs=100, verbose=1)

# # Function to predict the next word
# def predict_next_word(text):
#     sequence = tokenizer.texts_to_sequences([text])[0]
#     padded_sequence = pad_sequences([sequence], maxlen=max_sequence_len-1, padding='pre')
#     prediction = model.predict(padded_sequence)
#     predicted_word_index = np.argmax(prediction)
#     predicted_word = tokenizer.index_word[predicted_word_index]
#     return predicted_word

# # Example of predicting the next word
# print(predict_next_word("What are you"))
