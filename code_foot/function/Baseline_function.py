# -*- coding: utf-8 -*-
"""
Created on Sat Mar  5 17:55:34 2022

@author: Antoine MICHEL
@description : calculation of the baseline between 2 points define on a graph
"""
import numpy as np


def baseline (force):
    #Calculation of the baseline
    baseline = np.mean(force) #mean between two points
    return baseline
