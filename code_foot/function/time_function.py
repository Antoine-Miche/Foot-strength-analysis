# -*- coding: utf-8 -*-
"""
Created on Sat Mar  5 17:57:21 2022

@author: Antoine MICHEL
@description : function use to change the time of each trial because sometimes the data brut didn't begin at 0, it depends of the labchart file
@return :new column of time in the pandas series MVC_file

Example:
import Test_Function_Time

import matplotlib.pyplot as plt
import numpy as np
from function.time_function import time

plt.plot (MVC_File[1])
fe=1000
time(MVC_File,fe)
number_MVC = np.where (MVC_File[0] == 0)
"""


def time (MVC_File,fe):
    value = []
    for i in range (len(MVC_File[0])):
        value.append(MVC_File[0][i])
    MVC_File [0][0]= 0 #initialisation of the first of the MVC_file point at 0 

    for timepoint in range(1,len(MVC_File [0])-1) : # 1 to the total length of the file
    #change next point == previous +0.001
        if value[timepoint+1]==round(value[timepoint]+(1/fe),3):
            MVC_File [0][timepoint] = MVC_File[0][timepoint-1]+(1/fe)#if the next point was lesser than the previous point put 0
        else:
            MVC_File [0][timepoint] = 0 #else the next point correspond to the previous point + 1/fe


    MVC_File [0][len(MVC_File[0])-1] = 0 #to simplify the last graph the last MVC_File point's was equal to 0

    return MVC_File