#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import Flask, request, jsonify
import pandas as pd
import tensorflow as tf  # or your deep learning framework of choice

app = Flask(__name__)

# Assuming your LSTM model takes sequences of shape (2400, 9)
SEQUENCE_LENGTH = 2400
FEATURES = 9

@app.route('/predict', methods=['POST'])
def predict():
    try:
        #data = request.get_json()
        dataframe = pd.read_csv('D:/Orange/Episafe/data_frequency/2400_data.csv')  # Assuming you pass the dataframe as a list
        # Ensure that the input dataframe has the correct shape
        if len(dataframe) != SEQUENCE_LENGTH or len(dataframe[0]) != FEATURES:
            return jsonify({'error': 'Invalid input shape'})

        # Preprocess the input data (you may need to normalize or scale the data)
        #preprocessed_data = preprocess_input(dataframe)

        # Load and use your LSTM model to make predictions
        model = load_lstm_model()  # Function to load your pre-trained model
        result = model.predict(dataframe)

        # Assuming your model outputs a probability score; you can threshold it for classification
        #threshold = 0.5
        #binary_predictions = [1 if p > threshold else 0 for p in predictions]

        return jsonify({'predictions': result})
    except Exception as e:
        return jsonify({'error': str(e)})

def preprocess_input(dataframe):
    # You may need to perform preprocessing steps like scaling or normalizing the data
    # Here, we assume no preprocessing for simplicity
    return dataframe

def load_lstm_model():
    # Load your pre-trained LSTM model here using your deep learning framework
    model_path = 'D:/Orange/Episafe/model_deployment/lstm_model_v2_081.h5'
    model = tf.keras.models.load_model(model_path)
    return model

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
