# -*- coding: utf-8 -*-
"""
Created on Sun Jul 21 19:32:34 2024

@author: PatrickDunn
"""

import pandas as pd

# Define the mappings for categorical variables
categorical_mappings = {
    'SMARTGoals': {'Set': 0, 'Not Set': 1},
    'HFSymptoms': {'Stable': 0, 'New or Worsening': 1},
    'MedicationAdherence': {'All the time': 0, 'Inconsistently': 1, 'I am not taking my medication as prescribed': 2},
    'ActionPlan': {'Following plan': 0, 'Inconsistent': 1, 'Not following plan': 2},
    'TreatmentGoal': {'At goal': 0, 'Improving, but not at goal': 1, 'Not making progress': 2},
    'GDMTStatus': {'Optimal': 0, 'Suboptimal': 1, 'Not on GDMT': 2}
}

# Create a sample DataFrame with categorical and quantitative variables
data = {
    'PatientID': [1, 2, 3, 4],
    'SMARTGoals': ['Set', 'Not Set', 'Set', 'Not Set'],
    'HFSymptoms': ['Stable', 'New or Worsening', 'Stable', 'New or Worsening'],
    'MedicationAdherence': ['All the time', 'Inconsistently', 'I am not taking my medication as prescribed', 'All the time'],
    'ActionPlan': ['Following plan', 'Inconsistent', 'Not following plan', 'Following plan'],
    'TreatmentGoal': ['At goal', 'Improving, but not at goal', 'Not making progress', 'At goal'],
    'GDMTStatus': ['Optimal', 'Suboptimal', 'Not on GDMT', 'Optimal'],
    'HeartRate': [72, 101, 88, 76],
    'BloodPressure': ['120/80', '140/90', '130/85', '125/82'],
    'Weight': [70.5, 85.0, 78.2, 68.3]
}

df = pd.DataFrame(data)

# Apply the mappings to convert categorical responses to numerical values
for column, mapping in categorical_mappings.items():
    df[column] = df[column].map(mapping)

# Calculate the score by summing the specified columns
df['score'] = df[['SMARTGoals', 'HFSymptoms', 'MedicationAdherence', 'ActionPlan', 'TreatmentGoal', 'GDMTStatus']].sum(axis=1)

# Create a new column for the recheck interval based on the score
def determine_recheck_interval(score):
    if score == 0:
        return 'Recheck in 4 weeks'
    elif score <= 2:
        return 'Recheck in 2 weeks'
    else:
        return 'Recheck in 1 week'

df['RecheckInterval'] = df['score'].apply(determine_recheck_interval)

print(df)


