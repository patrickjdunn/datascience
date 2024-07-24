# -*- coding: utf-8 -*-
"""
Created on Sat Jul 13 14:15:33 2024

@author: PatrickDunn
"""

import numpy as np
from scipy import stats
# Sample data
data = [5.1, 4.8, 5.3, 5.7, 5.2, 4.9, 5.4, 5.6, 5.0, 5.3]
# Hypothesized population mean
mu = 5.0
# Perform one-sample t-test
t_stat, p_value = stats.ttest_1samp(data, mu)
# Print the result
print(f'T-statistic: {t_stat}')
print(f'P-value: {p_value}')
