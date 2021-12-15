import numpy as np
import pandas as pd
import seaborn as sns
import os
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
import matplotlib.pyplot as plt
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.metrics import f1_score
from sklearn.metrics import r2_score
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.metrics import f1_score
from sklearn.metrics import r2_score
from sklearn.preprocessing import LabelEncoder
import manipolazione
import lettura_dati
from sklearn import preprocessing

def splitTrainVal(data, percentualeSplit = 0.8):
    dataShuffled = data.copy().sample(frac=1) #shuffle
    size = len(dataShuffled)
    breakpoint = int(size * percentualeSplit)
    data = dataShuffled.iloc[0:breakpoint, :]
    val = dataShuffled.iloc[breakpoint:size, :]
    return data, val    

def getOversampling(data, osmCol):
    dataPresent = data[data[osmCol] == True]
    dataAbsent = data[data[osmCol] == False]
    
    proporzioneClassi = int(len(dataAbsent)/len(dataPresent))
    dataPresentOver = pd.concat([dataPresent] * proporzioneClassi)
    
    dataBalanced = pd.concat([dataPresentOver, dataAbsent])
    dataBalanced = dataBalanced.sample(frac=1) # shuffle
    return dataBalanced

def splitXY(stb_data, osmCol):
    x = stb_data.drop(columns = osmCol)
    y = stb_data[[osmCol]]
    return x, y

def mt_accuracy(y_true, y_pred):
    from sklearn.metrics import accuracy_score
    return accuracy_score(y_true, y_pred)
def mt_ce(y_true, y_pred):
    return (1-mt_accuracy(y_true, y_pred))

def print_metrics(y_true, y_pred):
    print("Accuracy: ", mt_accuracy(y_true, y_pred))
    print("CE: ", mt_ce(y_true, y_pred))
    print("Precision: ", precision_score(y_true, y_pred))
    print("Recall: ", recall_score(y_true, y_pred))
    print("F1: ", f1_score(y_true, y_pred))

def plot_feature_importances(xCols, mod):
    n_features = len(xCols)
    plt.barh(range(n_features), mod.feature_importances_, align='center')
    plt.yticks(np.arange(n_features), xCols)
    plt.xlabel("Feature importance")
    plt.ylabel("Feature")

def encodingStringhe(stb_data):
    for col in stb_data.columns:
        if (stb_data[col].dtype == "object"):
            encoder = LabelEncoder()
            stb_data[col] = encoder.fit_transform(stb_data[col])

def encodingY(stb_data, osmCol):
    stb_data[osmCol] = stb_data[osmCol].apply(lambda counter: True if counter > 0 else False)
    encoder = LabelEncoder()
    stb_data[osmCol] = encoder.fit_transform(stb_data[osmCol])

def getModelloRandForest(xTrain, yTrain):
    mod = RandomForestClassifier(n_estimators=100, criterion = "gini", max_features = 'auto')
    mod.fit(xTrain, yTrain.values.ravel())
    return mod

def printFeatures(xCols, mod):
    for i, j in zip(xCols, mod.feature_importances_):
        print(i, j)

def scaling(stb_data, osmCol):
    cols = stb_data.columns.drop(osmCol)
    stb_data[cols] = preprocessing.StandardScaler().fit_transform(stb_data[cols])

def prevediOsm(stb_data, osmCol):
    manipolazione.preparaDatiPerPredizione(stb_data)
    stati_data = stb_data[lettura_dati.getStatiCols(stb_data)]
    stati_data[osmCol] = stb_data[osmCol]
    
    encodingStringhe(stati_data)
    encodingY(stati_data, osmCol)

    scaling(stati_data, osmCol)
    train, val = splitTrainVal(stati_data)
    train = getOversampling(train, osmCol)

    xTrain, yTrain = splitXY(train, osmCol)
    xVal, yVal = splitXY(val, osmCol)

    xCols = xTrain.columns

    imp = SimpleImputer(missing_values=np.nan, strategy='mean')
    imp = imp.fit(xTrain)
    xTrain = imp.transform(xTrain)
    xVal = imp.transform(xVal)

    mod = getModelloRandForest(xTrain, yTrain)
    yPred = mod.predict(xVal)
    print_metrics(yVal, yPred)
    print("---")
    printFeatures(xCols, mod)