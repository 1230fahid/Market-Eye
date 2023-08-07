import json
import sklearn
import http.client
import numpy as np
import pandas as pd
import tensorflow as tf
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras import Sequential
from tensorflow.keras.layers import LSTM
from tensorflow.keras.layers import Dense

conn = http.client.HTTPSConnection("alpha-vantage.p.rapidapi.com")
headers = {
    'X-RapidAPI-Key': "2d9682785bmsh125a8783b4d4e57p1db292jsnc2cd9580c1c8",
    'X-RapidAPI-Host': "alpha-vantage.p.rapidapi.com"
}

conn.request("GET", "/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol=MSFT&outputsize=full&datatype=json", headers=headers)
res = conn.getresponse()
data = res.read()


conn = http.client.HTTPSConnection("alpha-vantage.p.rapidapi.com")
headers = {
    'X-RapidAPI-Key': "2d9682785bmsh125a8783b4d4e57p1db292jsnc2cd9580c1c8",
    'X-RapidAPI-Host': "alpha-vantage.p.rapidapi.com"
}

conn.request("GET", "/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol=MSFT&outputsize=full&datatype=json", headers=headers)
res = conn.getresponse()
data = res.read()
json_obj = json.loads(data.decode("utf-8"))  #ensures only one API call so we don't go over limit


SEARCH_PARAMS = {
    'epochs': 4,   #done
    'batch_size': 1, #done
    'look_back': 252, #done
    'lstm_layers':1, #done
    'lstm_neurons':1, #done
    'dense_layers':1,  #more layers can improve overall accuracy. Can lead to overfitting so needs to be controlled #done
    'dense_neurons':1, #same for more nodes. Can also lead to overfitting so need to be controlled #done
    'dropout':0.0  #used to help avoid overfitting
}

def train_evaluate(search_params):

    #print(f"epochs is {search_params['epochs']}")
    #print(f"batch_size is {search_params['batch_size']}")
    #print(f"look_back is {search_params['look_back']}")
    #print(f"lstm_layers is {search_params['lstm_layers']}")
    #print(f"lstm_neurons is {search_params['lstm_neurons']}")
    #print(f"dense_layers is {search_params['dense_layers']}")
    #print(f"dense_neurons is {search_params['dense_neurons']}")
    #print(f"dropout is {search_params['dropout']}")

    input_data = []
    json_data = json_obj['Time Series (Daily)']
    for date in json_data.keys():
        input_data.append([float(json_data[date]['1. open']), float(json_data[date]['2. high']), float(json_data[date]['3. low']), float(json_data[date]['4. close']), float(json_data[date]['5. adjusted close'])])

    input_data = input_data[:min(len(input_data), 2520)] #number of trading days in five years on average for NYSE and NASDAQ or less if not 5 years since stock was created.
    input_data = input_data[::-1]

    #set random seed to not change results
    tf.random.set_seed(1234)

    ### Data Preparation
    #convert to numpy array
    df = np.array(input_data)
    df = df.astype('float32')

    numpy_df = df

    #split into train and test sets
    train_size = int(len(numpy_df) * 0.67)
    test_size = len(numpy_df) - train_size
    trainOpen, testOpen = np.array(numpy_df [0:train_size,0]), np.array(numpy_df[train_size:,0])

    #reshape arrays
    trainOpen = np.reshape(trainOpen, (train_size, 1))
    testOpen = np.reshape(testOpen, (test_size, 1))


    #Use MinMaxScaler to normalize data
    scaler = MinMaxScaler(feature_range=(0, 1))
    trainOpen = scaler.fit_transform(trainOpen)
    testOpen = scaler.fit_transform(testOpen)


    #convert an array of values into a dataset matrix
    def create_dataset(data, look_back=1): #data is a numpy array and look_back refers to previous time steps. Both used as input variables for predicting the next time period
        dataX, dataY = [], []
        for i in range(len(data)-look_back):
            a = data[i:(i+look_back), 0]
            dataX.append(a)
            dataY.append(data[i+look_back, 0])
        return np.array(dataX), np.array(dataY)



    #reshape into X=t and Y=t+look_back. So we use current data with however many previous time steps and generate data for next time period
    look_back = search_params['look_back'] #try one year
    trainOpenX, trainOpenY = create_dataset(trainOpen, look_back) #basically trainX is the data used to predict trainY at each iteration. Each data in trainX is an array containing data from a current index i to i+look_back-1 inclusive. Then it's all used to predict the data at i+look_back
    testOpenX, testOpenY = create_dataset(testOpen, look_back)

    #reshape data in the form of [samples, time steps, features]
    trainOpenX = np.reshape(trainOpenX, (trainOpenX.shape[0], trainOpenX.shape[1], 1))
    testOpenX = np.reshape(testOpenX, (testOpenX.shape[0], testOpenX.shape[1], 1))

    def createModel():
        model = Sequential() #Sequential is how we can connect different types of layers
        for i in range(0, search_params['lstm_layers']):
            model.add(LSTM(search_params['lstm_neurons'], input_shape = (search_params['look_back'], 1), dropout=search_params['dropout'], return_sequences=True)) #LSTM 
        model.add(LSTM(search_params['lstm_neurons'], input_shape = (search_params['look_back'], 1), dropout=search_params['dropout'])) #LSTM 
        for i in range(0, search_params['dense_layers']):
            model.add(Dense(search_params['dense_neurons'])) #output layer with linear output
        model.add(Dense(1))
        model.compile(loss='mean_squared_error', optimizer='adam')
        return model

    def predict(model, trainInput, trainOutput, testInput, testOutput):
        #reset_model(model)
        #print(f"trainInput.size is ({len(trainInput)}, {len(trainInput[0])}, {len(trainInput[0][0])})")
        model.fit(trainInput, trainOutput, epochs=search_params['epochs'], batch_size=search_params['batch_size'], verbose=2)
        predicted_values_train = model.predict(trainInput)
        predicted_values_test = model.predict(testInput)
        #print(f"predicted_values_train.shape is ({len(predicted_values_train)}, {len(predicted_values_train[0])})")
        #print(f"predicted_values_test.shape is ({len(predicted_values_test)}, {len(predicted_values_test[0])})")
        score = model.evaluate(testInput, testOutput)
        return predicted_values_train, predicted_values_test, score

    newModel1 = createModel()
    predicted_values_train_open, predicted_values_test_open, open_score = predict(newModel1, trainOpenX, trainOpenY, testOpenX, testOpenY)

    return open_score

if __name__ == "__main__":
    scores = train_evaluate(SEARCH_PARAMS)
    print('validation AUC:', scores)
    