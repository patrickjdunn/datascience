# -*- coding: utf-8 -*-
"""
Created on Fri Jul 12 08:12:10 2024

@author: PatrickDunn
"""

import numpy as np
import pandas as pd
import statsmodels.api as sm
from statsmodels.formula.api import ols
from statsmodels.stats.anova import AnovaRM

# Example data: Repeated measures on three different conditions
data = pd.DataFrame({
    'subject': np.repeat(np.arange(1, 11), 3),
    'condition': np.tile(['A', 'B', 'C'], 10),
    'score': [5, 6, 7, 6, 7, 8, 5, 5, 6, 6, 6, 7, 7, 8, 9, 6, 6, 7, 8, 9, 9, 5, 6, 7, 4, 5, 6, 6, 7, 8]
})

# Perform repeated measures ANOVA
aovrm = AnovaRM(data, 'score', 'subject', within=['condition'])
fit = aovrm.fit()

# Print the ANOVA table
print(fit)

# Mauchly's Test of Sphericity
from statsmodels.stats.anova import mauchly

# Create a wide format data frame
data_wide = data.pivot(index='subject', columns='condition', values='score')

# Perform Mauchly's Test
mauchly_test = mauchly(data_wide)

print("Mauchly's Test of Sphericity:")
print(f'W: {mauchly_test[0]}, p-value: {mauchly_test[1]}')
