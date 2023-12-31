from flask import Flask, request, jsonify,render_template
import pandas as pd
import tensorflow as tf  # or your deep learning framework of choice
import numpy as np

app = Flask(__name__,template_folder='D:/Orange/Episafe/model_deployment/templates/')

# Assuming the LSTM model takes sequences of shape (2400, 9)
SEQUENCE_LENGTH = 2400
FEATURES = 9

@app.route('/index')
def index():
    return render_template('upload.html')  # Render an HTML form for file upload

@app.route('/predict', methods=['POST','GET'])
def predict():
    try:
        # Read the uploaded CSV file
        uploaded_file = request.files['csv_file']
        if uploaded_file == '':
            return jsonify({'error': 'file not uploaded'})
        #dataframe = pd.read_parquet('D:/Orange/Episafe_local/data/parquet/train/1869/014/UTC-2019_11_26-05_10_00.parquet')
        
        dataframe = pd.read_csv(uploaded_file)
        print(dataframe)
        #data preprocessing
        preprocessed_data = preprocess_input(dataframe)
        #check for data shape
        if len(preprocessed_data) != SEQUENCE_LENGTH or len(preprocessed_data[0]) != FEATURES:
            return jsonify({'error': 'Invalid input shape'})
        #make prediction
        print(preprocessed_data.shape)
        result = make_prediction(preprocessed_data)
        print(result)
        return render_template('result.html', predictions=result)
        
           # return jsonify({'error': 'file not uploaded'})
        #return jsonify({'predictions': result})
    except Exception as e:
        return jsonify({'error': str(e)})


def preprocess_input(df):
    df['timestamp'] = pd.to_datetime(df['utc_timestamp'], unit='s')

    # Set the timestamp column as the DataFrame index
    df.set_index('timestamp', inplace=True)

    # Create a new DataFrame with a datetime index at 4 Hz intervals
    resampled_df = pd.DataFrame(index=pd.date_range(start=df.index.min(), end=df.index.max(), freq='250L'))

    # Use groupby to resample the original data to 4 Hz (128 Hz / 32 = 4 Hz)
    for column in df.columns:
        resampled_df[column] = df[column].groupby(pd.Grouper(freq='250L')).mean()
    
    resampled_df['date_time'] = resampled_df.index
    resampled_df['timestamp_column'] = resampled_df['date_time'].apply(lambda x: pd.Timestamp(x).timestamp())
    resampled_df.reset_index(inplace=True)
    resampled_df.drop(['utc_timestamp','date_time','index'],axis=1,inplace=True)
    return np.array(resampled_df)

def load_lstm_model():
    # Load your pre-trained LSTM model here using your deep learning framework
    model_path = 'D:/Orange/Episafe/model_deployment/lstm_model_v2_081.h5'
    model = tf.keras.models.load_model(model_path)
    return model

def make_prediction(data):
    model = load_lstm_model()
    prediction_result = model.predict(np.expand_dims(data, axis=0))
    threshold = 0.5
    binary_prediction = [1 if prediction_result > threshold else 0 ]
    return binary_prediction

if __name__ == '__main__':
    app.run(debug=True)
