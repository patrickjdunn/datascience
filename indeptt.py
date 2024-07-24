# -*- coding: utf-8 -*-
"""
Created on Sat Jul 13 14:17:54 2024

@author: PatrickDunn
"""

import numpy as np
from scipy import stats
# Sample data
group1 = [5.1, 4.8, 5.3, 5.7, 5.2, 4.9, 5.4, 5.6, 5.0, 5.3]
group2 = [4.7, 4.6, 4.8, 4.9, 5.1, 4.5, 4.6, 4.7, 4.8, 4.9]
# Perform independent samples t-test
t_stat, p_value = stats.ttest_ind(group1, group2)
# Print the result
print(f'T-statistic: {t_stat}')
print(f'P-value: {p_value}')
