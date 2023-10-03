import pandas as pd
import numpy as np
import tensorflow as tf

data = pd.read_csv('C:/Users/jihed/OneDrive/Bureau/testing_file.csv')

def change_frequency(df):
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
    return resampled_df

X_test = change_frequency(data)
X_test2 = np.array(X_test)
"""print (X_test)
print (X_test2)
print(X_test2.shape)"""




model_path = 'D:/Orange/Episafe/model_deployment/lstm_model_v2_081.h5'


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

decision = make_prediction(X_test2)
print(decision)
