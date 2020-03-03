# -*- coding: utf-8 -*-
"""
Created on Mon Jan 21 16:05:27 2019

@author: hammi
"""

import pandas as pd
import numpy as np

def cleanData(dataFrame):
    df = pd.read_csv(dataFrame)
    df_clean = df.dropna()
    return df_clean
