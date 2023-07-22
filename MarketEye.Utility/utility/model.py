import sys
import json
import pyodbc
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


class Model:
    def __init__(self):
        self.__search_parameters = {    
            'epochs': 8,
            'batch_size': 79, #batch size refers to number of samples per gradient update. Batch gradient descent
            'look_back': 105,
            'lstm_layers':0,
            'lstm_neurons':41,
            'dense_layers':0,  #more layers can improve overall accuracy. Can lead to overfitting so needs to be controlled
            'dense_neurons':1, #same for more nodes. Can also lead to overfitting so need to be controlled
            'dropout': 0.03266834992122359  #used to help avoid overfitting
        }
        self.__stock_data = []
        self.__dataframe = None
        self.__train_size = 0
        self.__test_size = 0
        self.__scaler = MinMaxScaler(feature_range=(0, 1))

    def __connect(self, stock="MSFT"):
        conn = http.client.HTTPSConnection("alpha-vantage.p.rapidapi.com")
        headers = {
            'X-RapidAPI-Key': "2d9682785bmsh125a8783b4d4e57p1db292jsnc2cd9580c1c8",
            'X-RapidAPI-Host': "alpha-vantage.p.rapidapi.com"
        }
        conn.request("GET", f"/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={stock}&outputsize=full&datatype=json", headers=headers)
        res = conn.getresponse()
        data = res.read()
        json_obj = json.loads(data.decode("utf-8"))
        self.__stock_data = []
        json_data = json_obj['Time Series (Daily)']
        for date in json_data.keys():
            self.__stock_data.append([float(json_data[date]['1. open']), float(json_data[date]['2. high']), float(json_data[date]['3. low']), float(json_data[date]['4. close']), float(json_data[date]['5. adjusted close'])])
        self.__stock_data = self.__stock_data[:min(len(self.__stock_data), 2520)] #number of trading days in five years on average for NYSE and NASDAQ or less if not 5 years since stock was created.
        self.__stock_data = self.__stock_data[::-1]
        return self.__stock_data
    

    def get_stock_data(self):
        return self.__stock_data

    def get_search_parameters(self):
        return self.__search_parameters
    
    def set_search_parameters(self, epochs, batch_size, look_back, lstm_layers, lstm_neurons, dense_layers, dense_neurons, dropout):
        self.__search_parameters = {
            'epochs': epochs,
            'batch_size': batch_size, #batch size refers to number of samples per gradient update. Batch gradient descent
            'look_back': look_back,
            'lstm_layers':lstm_layers,
            'lstm_neurons':lstm_neurons,
            'dense_layers':dense_layers,  #more layers can improve overall accuracy. Can lead to overfitting so needs to be controlled
            'dense_neurons':dense_neurons, #same for more nodes. Can also lead to overfitting so need to be controlled
            'dropout': dropout  #used to help avoid overfitting
        }
    
    def __data_preparation(self, input_data):
        ### Data Preparation
        numpy_df = np.array(input_data)
        numpy_df = numpy_df.astype('float32')
        self.__train_size = int(len(numpy_df) * 0.67)
        self.__test_size = len(numpy_df) - self.__train_size
        self.__dataframe = numpy_df
    
    def view_trends(self):
        # Let's see a historical view of the closing price
        ax = plt.GridSpec(2, 3)
        ax.update(wspace=1, hspace=1)
        axis1 = plt.subplot(ax[0,0])
        axis2 = plt.subplot(ax[0,1])
        axis3 = plt.subplot(ax[0,2])
        axis4 = plt.subplot(ax[1,:2])
        axis5 = plt.subplot(ax[1,2:])
        axis1.plot(self.__dataframe[:,0])
        axis1.set_title("Open Price History")
        axis2.plot(self.__dataframe[:,1])
        axis2.set_title("High Price History")
        axis3.plot(self.__dataframe[:,2])
        axis3.set_title("Low Price History")
        axis4.plot(self.__dataframe[:,3])
        axis4.set_title("Close Price History")
        axis5.plot(self.__dataframe[:,4])
        axis5.set_title("Adj Close Price History")
        plt.show()

    def __split_data(self, col):
        train, test = np.array(self.__dataframe[0:self.__train_size,col]), np.array(self.__dataframe[self.__train_size:,col])
        train = np.reshape(train, (self.__train_size, 1))
        test = np.reshape(test, (self.__test_size, 1))
        return train, test
    
        #convert an array of values into a dataset matrix
    def __create_dataset(self, data, look_back=1): #data is a numpy array and look_back refers to previous time steps. Both used as input variables for predicting the next time period
        dataX, dataY = [], []
        for i in range(len(data)-look_back):
            a = data[i:(i+look_back), 0]
            dataX.append(a)
            dataY.append(data[i+look_back, 0])
        return np.array(dataX), np.array(dataY)

    def __lstm(self):
        trainOpen, testOpen = self.__split_data(0)
        trainHigh, testHigh = self.__split_data(1)
        trainLow, testLow = self.__split_data(2)
        trainClose, testClose = self.__split_data(3)
        trainAdjustedClose, testAdjustedClose = self.__split_data(4)
        trainOpen = self.__scaler.fit_transform(trainOpen)
        trainHigh = self.__scaler.fit_transform(trainHigh)
        trainLow = self.__scaler.fit_transform(trainLow)
        trainClose = self.__scaler.fit_transform(trainClose)
        trainAdjustedClose = self.__scaler.fit_transform(trainAdjustedClose)
        testOpen = self.__scaler.fit_transform(testOpen)
        testHigh = self.__scaler.fit_transform(testHigh)
        testLow = self.__scaler.fit_transform(testLow)
        testClose = self.__scaler.fit_transform(testClose)
        testAdjustedClose = self.__scaler.fit_transform(testAdjustedClose)

        #reshape into X=t and Y=t+look_back. So we use current data with however many previous time steps and generate data for next time period
        look_back = self.__search_parameters['look_back'] #try one year
        trainOpenX, trainOpenY = self.__create_dataset(trainOpen, look_back) #basically trainX is the data used to predict trainY at each iteration. Each data in trainX is an array containing data from a current index i to i+look_back-1 inclusive. Then it's all used to predict the data at i+look_back
        testOpenX, testOpenY = self.__create_dataset(testOpen, look_back)
        trainHighX, trainHighY = self.__create_dataset(trainHigh, look_back) #basically trainX is the data used to predict trainY at each iteration. Each data in trainX is an array containing data from a current index i to i+look_back-1 inclusive. Then it's all used to predict the data at i+look_back
        testHighX, testHighY = self.__create_dataset(testHigh, look_back)
        trainLowX, trainLowY = self.__create_dataset(trainLow, look_back) #basically trainX is the data used to predict trainY at each iteration. Each data in trainX is an array containing data from a current index i to i+look_back-1 inclusive. Then it's all used to predict the data at i+look_back
        testLowX, testLowY = self.__create_dataset(testLow, look_back)
        trainCloseX, trainCloseY = self.__create_dataset(trainClose, look_back) #basically trainX is the data used to predict trainY at each iteration. Each data in trainX is an array containing data from a current index i to i+look_back-1 inclusive. Then it's all used to predict the data at i+look_back
        testCloseX, testCloseY = self.__create_dataset(testClose, look_back)
        trainAdjustedCloseX, trainAdjustedCloseY = self.__create_dataset(trainAdjustedClose, look_back) #basically trainX is the data used to predict trainY at each iteration. Each data in trainX is an array containing data from a current index i to i+look_back-1 inclusive. Then it's all used to predict the data at i+look_back
        testAdjustedCloseX, testAdjustedCloseY = self.__create_dataset(testAdjustedClose, look_back)

        #reshape data in the form of [samples, time steps, features]
        trainOpenX = np.reshape(trainOpenX, (trainOpenX.shape[0], trainOpenX.shape[1], 1))
        testOpenX = np.reshape(testOpenX, (testOpenX.shape[0], testOpenX.shape[1], 1))
        trainHighX = np.reshape(trainHighX, (trainHighX.shape[0], trainHighX.shape[1], 1))
        testHighX = np.reshape(testHighX, (testHighX.shape[0], testHighX.shape[1], 1))
        trainLowX = np.reshape(trainLowX, (trainLowX.shape[0], trainLowX.shape[1], 1))
        testLowX = np.reshape(testLowX, (testLowX.shape[0], testLowX.shape[1], 1))
        trainCloseX = np.reshape(trainCloseX, (trainCloseX.shape[0], trainCloseX.shape[1], 1))
        testCloseX = np.reshape(testCloseX, (testCloseX.shape[0], testCloseX.shape[1], 1))
        trainAdjustedCloseX = np.reshape(trainAdjustedCloseX, (trainAdjustedCloseX.shape[0], trainAdjustedCloseX.shape[1], 1))
        testAdjustedCloseX = np.reshape(testAdjustedCloseX, (testAdjustedCloseX.shape[0], testAdjustedCloseX.shape[1], 1))

        open_model, predicted_values_train_open, predicted_values_test_open, open_score = self.__train_data(trainOpenX, trainOpenY, testOpenX, testOpenY)
        high_model, predicted_values_train_high, predicted_values_test_high, high_score = self.__train_data(trainHighX, trainHighY, testHighX, testHighY)
        low_model, predicted_values_train_low, predicted_values_test_low, low_score = self.__train_data(trainLowX, trainLowY, testLowX, testLowY)
        close_model, predicted_values_train_close, predicted_values_test_close, close_score = self.__train_data(trainCloseX, trainCloseY, testCloseX, testCloseY)
        adj_close_model, predicted_values_train_adj_close, predicted_values_test_adj_close, adj_close_score = self.__train_data(trainAdjustedCloseX, trainAdjustedCloseY, testAdjustedCloseX, testAdjustedCloseY)                

        predicted_values_test_open_prices = self.__scaler.inverse_transform(predicted_values_test_open)
        predicted_values_test_high_prices = self.__scaler.inverse_transform(predicted_values_test_high)
        predicted_values_test_low_prices = self.__scaler.inverse_transform(predicted_values_test_low)
        predicted_values_test_close_prices = self.__scaler.inverse_transform(predicted_values_test_close)
        predicted_values_test_adj_close_prices = self.__scaler.inverse_transform(predicted_values_test_adj_close)

        testOpenY = np.reshape(testOpenY, (len(testOpenY),1))
        testHighY = np.reshape(testHighY, (len(testHighY),1))
        testLowY = np.reshape(testLowY, (len(testLowY),1))
        testCloseY = np.reshape(testCloseY, (len(testCloseY),1))
        testAdjustedCloseY = np.reshape(testAdjustedCloseY, (len(testAdjustedCloseY),1))

        actual_values_test_open_prices = self.__scaler.inverse_transform(testOpenY)
        actual_values_test_high_prices = self.__scaler.inverse_transform(testHighY)
        actual_values_test_low_prices = self.__scaler.inverse_transform(testLowY)
        actual_values_test_close_prices = self.__scaler.inverse_transform(testCloseY)
        actual_values_test_adj_close_prices = self.__scaler.inverse_transform(testAdjustedCloseY)

        rmse_test_open = np.sqrt(np.mean(((actual_values_test_open_prices - predicted_values_test_open_prices) ** 2)))
        rmse_test_high = np.sqrt(np.mean(((actual_values_test_high_prices - predicted_values_test_high_prices) ** 2)))
        rmse_test_low = np.sqrt(np.mean(((actual_values_test_low_prices - predicted_values_test_low_prices) ** 2)))
        rmse_test_close = np.sqrt(np.mean(((actual_values_test_close_prices - predicted_values_test_close_prices) ** 2)))
        rmse_test_adj_close = np.sqrt(np.mean(((actual_values_test_adj_close_prices - predicted_values_test_adj_close_prices) ** 2)))
        print(f"rmse_test_open is {rmse_test_open}")
        print(f"rmse_test_high is {rmse_test_high}")
        print(f"rmse_test_low is {rmse_test_low}")
        print(f"rmse_test_close is {rmse_test_close}")
        print(f"rmse_test_adj_close is {rmse_test_adj_close}")

        today_test_open = np.array([testOpen[len(testOpen)-look_back:,0]])
        today_test_open = np.reshape(today_test_open, (today_test_open.shape[0], today_test_open.shape[1], 1))
        tmr_prediction_open = open_model.predict(today_test_open)
        tmr_prediction_open_price = self.__scaler.inverse_transform(tmr_prediction_open)

        today_test_high = np.array([testHigh[len(testHigh)-look_back:,0]])
        today_test_high = np.reshape(today_test_high, (today_test_high.shape[0], today_test_high.shape[1], 1))
        tmr_prediction_high = high_model.predict(today_test_high)
        tmr_prediction_high_price = self.__scaler.inverse_transform(tmr_prediction_high)

        today_test_low = np.array([testLow[len(testLow)-look_back:,0]])
        today_test_low = np.reshape(today_test_low, (today_test_low.shape[0], today_test_low.shape[1], 1))
        tmr_prediction_low = low_model.predict(today_test_low)
        tmr_prediction_low_price = self.__scaler.inverse_transform(tmr_prediction_low)

        today_test_close = np.array([testClose[len(testClose)-look_back:,0]])
        today_test_close = np.reshape(today_test_close, (today_test_close.shape[0], today_test_close.shape[1], 1))
        tmr_prediction_close = close_model.predict(today_test_close)
        tmr_prediction_close_price = self.__scaler.inverse_transform(tmr_prediction_close)

        today_test_adj_close = np.array([testAdjustedClose[len(testAdjustedClose)-look_back:,0]])
        today_test_adj_close = np.reshape(today_test_adj_close, (today_test_adj_close.shape[0], today_test_adj_close.shape[1], 1))
        tmr_prediction_adj_close = adj_close_model.predict(today_test_adj_close)
        tmr_prediction_adj_close_price = self.__scaler.inverse_transform(tmr_prediction_adj_close)
        return tmr_prediction_open_price[0][0], tmr_prediction_high_price[0][0], tmr_prediction_low_price[0][0], tmr_prediction_close_price[0][0], tmr_prediction_adj_close_price[0][0]

    def __createModel(self):
        tf.keras.backend.clear_session()
        model = Sequential() #Sequential is how we can connect different types of layers
        for i in range(0, self.__search_parameters['lstm_layers']):
            model.add(LSTM(self.__search_parameters['lstm_neurons'], input_shape = (self.__search_parameters['look_back'], 1), dropout=self.__search_parameters['dropout'], return_sequences=True)) #LSTM 
        model.add(LSTM(self.__search_parameters['lstm_neurons'], input_shape = (self.__search_parameters['look_back'], 1))) #LSTM 
        for i in range(0, self.__search_parameters['dense_layers']):
            model.add(Dense(self.__search_parameters['dense_neurons'])) #output layer with linear output
        model.add(Dense(1)) #output layer with linear output
        model.compile(loss='mean_squared_error', optimizer='adam')
        return model
    
    def __predict(self, model, trainInput, trainOutput, testInput, testOutput):
        model.fit(trainInput, trainOutput, epochs=self.__search_parameters['epochs'], batch_size=self.__search_parameters['batch_size'], verbose=2)
        predicted_values_train = model.predict(trainInput)
        predicted_values_test = model.predict(testInput)
        newTrainOutput = np.reshape(trainOutput, (len(trainOutput), 1))
        score = model.evaluate(x=testInput, y=testOutput)
        return predicted_values_train, predicted_values_test, score

    def __train_data(self, trX, trY, teX, teY):
        newModel = self.__createModel()
        predicted_values_train, predicted_values_test, score = self.__predict(newModel, trX, trY, teX, teY)
        return newModel, predicted_values_train, predicted_values_test, score

    def __se(self, predicted, actual):
        total = 0
        for i in range(len(predicted)):
            total += (predicted[i] - actual[i]) ** 2
        return total

    def run(self, tick="MSFT"):
        data = self.__connect(tick)
        self.__data_preparation(data)
        return self.__lstm()

def return_bytes(the_bytes):
    return the_bytes


if __name__ == "__main__":

    cnxn = pyodbc.connect('Driver={ODBC Driver 18 for SQL Server};'
                          'SERVER=LAPTOP-S2FR70QO\\SQLEXPRESS;'
                          'DATABASE=Market_Eye;'
                          'ENCRYPT=yes;'
                          'Trusted_Connection=yes;'
                          'TrustServerCertificate=yes;')
    cursor = cnxn.cursor()
    cursor.execute('SELECT * FROM AspNetUsers')

    cnxn.add_output_converter(-155, return_bytes)
    row = cursor.fetchone() 
    while row: 
        print(row)
        row = cursor.fetchone()
    stockDict = {}
    stocks = ["HVAL", "JOJO"]
    tf.random.set_seed(1234)
    model = Model()

    for stock in stocks:
        tmr_open, tmr_high, tmr_low, tmr_close, tmr_adj_close = model.run(stock)
        array = [tmr_open, tmr_high, tmr_low, tmr_close, tmr_adj_close]
        minVal = min(array)
        minIdx = array.index(minVal)
        if minIdx != 2:
            array[2], array[minIdx] = array[minIdx], array[2]
        maxVal = max(array)
        maxIdx = array.index(maxVal)
        if maxIdx != 1:
            array[1], array[maxIdx] = array[maxIdx], array[1]
        stockDict[stock] = array

    for stock in stockDict.keys():
        print(f"stockDict[{stock}] is\n{stockDict[stock]}")
