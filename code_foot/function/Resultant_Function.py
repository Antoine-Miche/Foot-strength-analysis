# -*- coding: utf-8 -*-
"""
Created on Sat Mar  5 17:55:43 2022

@author: Antoine MICHEL
@description : calculation of the force resultant, and put the value in a list
@return : resultant list with the value ofthe force resultant

Example:
"""
   
""" 
import test_function_resultant
"""
"""
from function.Resultant_Function import resultant
resultantlist = []
increment = 0
resultant (data,increment,resultantlist)
"""
import numpy as np


def resultant (list1, increment, resultantlist):
    #calculation of the force resultant 
    time = list1[increment][-1].time.astype(float) #put the time in a variable
    Fz = list1[increment][-1].Fz.astype(float) #put Fz in a variable
    Fy = list1[increment][-1].Fy.astype(float) #put Fy in a variable
    Fx = list1[increment][-1].Fx.astype(float) #put Fx in a variable
    comment = list1[increment][-1].comments #put labchartFile's comments in a variable
    Fxyz = np.sqrt ((Fz**2)+(Fx**2)+(Fy**2)) #create a variable of the resultant vector xyz
    Fyz = np.sqrt ((Fz**2)+(Fy**2)) #create a variable of the resultant vector Fyz
    dataUse= [list1[increment][0],list1[increment][1],list1[increment][2],list1[increment][3],time,Fz, Fy, Fx, Fyz, Fxyz, comment]#create a list with all the variable for one file
    resultantlist.append (dataUse) #put the list of one file in a global list to obtain all the data for all the file
    return resultantlist