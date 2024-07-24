# -*- coding: utf-8 -*-
"""
Created on Fri Jul 12 08:32:07 2024

@author: PatrickDunn
"""

import pandas as pd
import statsmodels.api as sm
from statsmodels.formula.api import ols

# Step 1: Prepare the Data
data = pd.DataFrame({
    'DietProgram': ['Control', 'Control', 'Control', 
                    'Low-Carb', 'Low-Carb', 'Low-Carb', 
                    'Low-Fat', 'Low-Fat', 'Low-Fat'],
    'WeightLoss': [3.0, 2.5, 2.8, 5.2, 4.9, 5.5, 4.0, 3.8, 4.1],
    'BaselineWeight': [85, 90, 88, 95, 93, 97, 80, 83, 82]
})

# Step 2: Run the ANCOVA
model = ols('WeightLoss ~ DietProgram + BaselineWeight', data=data).fit()
ancova_table = sm.stats.anova_lm(model, typ=2)

# Output the result
print(ancova_table)
