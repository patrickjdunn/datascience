# -*- coding: utf-8 -*-
"""
Created on Fri Jul 12 08:20:33 2024

@author: PatrickDunn
"""

import pandas as pd
from scipy.stats import f_oneway

# Step 1: Prepare the Data
data = {
    'AgeGroup': ['18-29', '18-29', '18-29', '30-44', '30-44', '30-44', 
                 '45-59', '45-59', '45-59', '60+', '60+', '60+'],
    'BMI': [22.5, 24.1, 23.0, 27.5, 26.3, 28.1, 29.2, 30.5, 28.9, 27.0, 26.4, 25.9]
}

df = pd.DataFrame(data)

# Step 2: Split the data by AgeGroup
grouped_data = df.groupby('AgeGroup')['BMI'].apply(list)

# Step 3: Run the One-Way ANOVA
anova_result = f_oneway(*grouped_data)

# Step 4: Output the result
print(f"F-statistic: {anova_result.statistic}")
print(f"p-value: {anova_result.pvalue}")
