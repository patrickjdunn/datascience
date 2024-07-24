# -*- coding: utf-8 -*-
"""
Created on Mon Jul 15 08:07:30 2024

@author: PatrickDunn
"""

import pandas as pd
from os import path
#import seaborn as sns
#import matplotlib.pyplot as plt

# change this to the directory where the csv files that come with the book are
# stored
# on Windows it might be something like 'C:/mydir'

#DATA_DIR = '/Users/PatrickDunn/LearningPy/data'
DATA_DIR = 'D:/YourHeartScore/DataScience/data/Python'

##############
# Loading data
##############
#cardio = pd.read_csv(path.join(DATA_DIR, 'mldata', 'cardio.csv'))
cardio = pd.read_csv(path.join(DATA_DIR, 'cardio.csv'))

type(cardio)

##################################
# DataFrame methods and attributes
##################################
cardio.head()


# Create a frequency table
disease_frequency = cardio['cardio'].value_counts()

# Print the frequency table
print(disease_frequency)

# Convert frequency table to DataFrame
disease_frequency_df = disease_frequency.reset_index()

# Rename columns for clarity
disease_frequency_df.columns = ['Disease_Type', 'Frequency']

# Print the DataFrame
print(disease_frequency_df)


