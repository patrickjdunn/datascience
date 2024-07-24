# -*- coding: utf-8 -*-
"""
Created on Fri Jul 12 08:37:13 2024

@author: PatrickDunn
"""

import pandas as pd
from statsmodels.multivariate.manova import MANOVA

# Step 1: Prepare the Data
data = pd.DataFrame({
    'ExerciseProgram': ['Control', 'Control', 'Control', 
                        'Cardio', 'Cardio', 'Cardio', 
                        'Strength', 'Strength', 'Strength'],
    'WeightLoss': [1.0, 0.5, 0.8, 3.0, 2.8, 3.2, 2.0, 1.8, 2.1],
    'CholesterolReduction': [5, 4, 6, 15, 14, 16, 10, 11, 12]
})

# Step 2: Run the MANOVA
manova = MANOVA.from_formula('WeightLoss + CholesterolReduction ~ ExerciseProgram', data)

# Output the result
manova_result = manova.mv_test()
print(manova_result)
