# -*- coding: utf-8 -*-
"""
Created on Thu Jul 18 17:04:53 2024

@author: PatrickDunn
"""

import pandas as pd
from os import path
import matplotlib.pyplot as plt
import seaborn as sns
import sklearn
import warnings

from sklearn.preprocessing import LabelEncoder
from sklearn.impute import KNNImputer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import f1_score
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import cross_val_score

warnings.filterwarnings('ignore')

DATA_DIR = 'D:/YourHeartScore/DataScience/data/Python'
cardio = pd.read_csv(path.join(DATA_DIR, 'cardio.csv'))
HLdata = pd.read_csv(path.join(DATA_DIR, 'HLdata.csv'))
df = pd.read_csv(path.join(DATA_DIR, 'Salaries.csv'))

#cardio.head()
#HLdata.head()
#df.head()

#df = pd.read_csv('Salaries.csv')
print(df)
