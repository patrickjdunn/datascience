# -*- coding: utf-8 -*-
"""
Created on Tue Jul 23 14:07:25 2024

@author: PatrickDunn
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Sample data
np.random.seed(123)
data = pd.DataFrame({
    'group': np.repeat(['Smoker', 'Non-Smoker'], 50),
    'cholesterol': np.concatenate([np.random.normal(200, 30, 50), np.random.normal(180, 25, 50)])
})

# View the first few rows of the data
print(data.head())

# Create a box plot
plt.figure(figsize=(10, 6))

# Use pandas to make the boxplot
data.boxplot(column='cholesterol', by='group', grid=False)

# Adding titles and labels
plt.title('Box Plot of Cholesterol Levels by Smoking Status')
plt.suptitle('')  # Suppress the default title to clean up the plot
plt.xlabel('Group')
plt.ylabel('Cholesterol Level')

# Show the plot
plt.show()

