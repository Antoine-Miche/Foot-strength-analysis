# -*- coding: utf-8 -*-
"""
Created on Sat Mar  5 17:54:38 2022

@author: Antoine MICHEL,

@title : analysis of MVC and RFD of the foot

@description : this file analyze the strength (MVIC) and the rate of force devlopment (RFID) of the foot, datas were recorded 
with an inovant ergometer. The RFID analysis was based on th paper of maffiuleti et al.2016. Futhermore, we analyzed different
componant of the strength Fz, Fy, Fx, and we analyzed also the resultant of the strength Fzy and Fzyx
"""

"""
@list of function:
wrapper_function(basepath,filelist)

resultant_function(list1, increment)

time_function(MVC or RFD_File list, fe)

Baseline_Function (force)

MVC_function(resultant, MVC_DataFrame, resultantlist, MVC_For_RFD, fe)
             ==> resultant : list of data brut for the MVC
             ==> MVC_DataFrame : Data_Frame to put the value
             ==>resultantlist : list to take the session the id and the foot
             ==> MVC_For_RFD : list for putting the max-min use for the RFD after
             ==> fe : samplig frequency

RFD_function(RFD_File, MVC,resultantlist, fe)
             ==>RFD_File : list of data brut for the RFD
             ==>MVC : best MVC for check the contraction
             ==>resultantlist : list to take the session the id and the foot
             ==>fe : samplig frequency
"""

"""
wrapper_function ==> input : (basepath,filelist)
@description : Take the file directly in the folder and put the value in a list with the partipant ID, foot, and session
output : list1 (list) with the ID, the Session, the foot, and the data
"""

"""
resultant_function ==> input : (list1(list return by the wrapper function), increment (increment of the forloop len == list1))
@description : calculation of the force resultant, and put the value in a list
output : list (resultantlist) with the id, the session, the foot, the data, and the resultant, for each file
"""

"""
time_function ==> input :(MVC or RFD_File list, fe(sampling frequency in Hz))
@description : function use to change the time of each trial because sometimes the data brut didn't 
begin at 0, it depends of the labchart file
output : return the MVC_file (list) with the new column of time
"""

"""
Baseline_Function ==> input : (force (between two points))
@description : calculation of the baseline between 2 points define on a graph
return a float (baseline) in N
"""

"""
MVC_function ==> input : (resultant, MVC_DataFrame, resultantlist, MVC_For_RFD, fe)
             ==> resultant : list of data brut for the MVC
             ==> MVC_DataFrame : Data_Frame to put the value
             ==>resultantlist : list to take the session the id and the foot
             ==> MVC_For_RFD : list for putting the max-min use for the RFD after
             ==> fe : samplig frequency in Hz
@description : function to analyze the maximal strength of each componant of the strength with graphical interaction
output ==>MVC_DataFrame ==> with the value of the mvc for each componant of the strength in (N)
       ==> MVC_For_RFD ==> list with the MVC max-min (N)
"""

"""
RFD_function ==> input : (RFD_File, MVC,resultantlist, fe)
             ==>RFD_File : list of data brut for the RFD
             ==>MVC : best MVC for check the contraction in N
             ==>resultantlist : list to take the session the id and the foot
             ==>fe : samplig frequency Hz
@description : function to analyze the rate of force devlopment of Fz, Fzy, Fzyx componant of the strength with 
graphical interaction
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os as os

from function.wrapper_function import wrapper
from function.Resultant_Function import resultant
from function.MVC_Function import MVC
from function.RFD_function import RFD

"""initialisation of different list"""
resultantlist = [] 
listerror_RFD = []
RFD_Value = []
For_RFD =[]

""""initialisation of the MVC DataFrame"""
MVC_DataFrame = pd.DataFrame(columns = ['Contraction_number', 'check','ID', 'Contraction_type', 'Session','foot','FMAXz', 
                'TimeMVCz','FMAXy','TimeMVCy', 'FMAXx', 'TimeMVCx', 'FMAXzy','TimeMVCzy', 
                'FMAXxyz','TimeMVCxyz'])


basepath = 'C:\\Users\\antoi\\Desktop\\test\\' # initialisation of the base path to take all the file
fe = 1000 #initialisation of the sampling rate

fileList = os.listdir(basepath) #take all the File in the folder
data = wrapper(basepath, fileList) #take only the txt file and put this file in a data list

""" this loop take the file in the data list and analyze each increment """
for i in range (len(data)) :
    resultant(data, i, resultantlist) #create a resultant list with all the value for each file
    
    """initialisation of list"""
    RFD_File = []
    MVC_File = []
    
    val = np.where (data[i][-1].comments.str.contains('#* rfd') == True)#create a numpy array to find where the comment == True the value == 1 if true 0 if false
    if len(val[0]) == 1: #if there is a value = 1  in the numpy array 
        for indx in range (4, 11) :
            MVC_File.append(resultantlist[i][indx][:val[0][0]]) #all the data before the comment
            RFD_File.append(resultantlist[i][indx][val[0][0]:]) #all the data after the comment
        
        MVC_For_RFD =[] #initialisation of a list wich take into account the MVC with the Max-Min like during the data acquisition
        MVC(MVC_File, MVC_DataFrame, resultantlist[i],MVC_For_RFD,fe)  #run the MVC analysis  see function MVC
        MVC_For_RFD = max (MVC_For_RFD) #take the maximal MVC for the file to be use for the RFD analysis
        For_RFD.append(MVC_For_RFD) # add MVC for another list of MVC
        plt.close('all') #close all the plot 
        
        for reindex in RFD_File:
            reindex.reset_index(drop = True, inplace = True)
        plt.close('all')
        """
        MVC_For_RFD = pd.read_csv(basepath + '\\Max_Min_FootP020a.csv', sep = ';',names = ['index', 'Max'], decimal = '.', low_memory=False)
        MVC_For_RFD = MVC_For_RFD.Max[1:len(MVC_For_RFD)].astype(float)
        """
        RFD(RFD_File, MVC_For_RFD[i],resultantlist[i],fe,listerror_RFD,RFD_Value)
        plt.close('all')
        
    print(i) #count the number of analysis performed 
"""
Max_Min = pd.DataFrame(For_RFD,columns = ['Max-Min'])#create a dataframe with the max-min MVC value usefull for the rfd to run only the analysis of the rfd if necessary
MVC_DataFrame.to_csv(basepath + '\\MVC_FootP020B.csv', sep = ';')#create the csv file for the MVC
Max_Min.to_csv(basepath + '\\Max_Min_FootP020B.csv', sep = ';')#create the csv file max-min MVC
"""
"""creation ofthe rfd's dataframe"""
df = pd.DataFrame(RFD_Value , columns = ['number', 'ID', 'Contraction_type', 'Session', 'foot',
                                        'Zman_Onset','Maxz', 'Zimp50man','Zslope50man',
                                        'Zimp100man','Zslope100man','Zimp200man','Zslope200man',
                                        'Zimp250man','Zslope250man','Zyman_Onset', 'Maxzy', 
                                        'Zyimp50man','Zyslope50man',
                                        'Zyimp100man','Zyslope100man','Zyimp200man','Zyslope200man',
                                         'Zyimp250man','Zyslope250man',
                                        'Zyxman_Onset', 'Maxzyx', 'Zyximp50man','Zyxslope50man',
                                        'Zyximp100man','Zyxslope100man','Zyximp200man','Zyxslope200man',
                                         'Zyximp250man', 'Zyxslope250man'])

df.to_csv(basepath + '\\RFD_FootP020B.csv', sep = ';')#save all the data of the rfd

ErrorDataFrame = pd.DataFrame(listerror_RFD, columns = ['contraction_number', 'ID', 'error_type','foot','session'])#save the good and the not good contraction with the reason

ErrorDataFrame.to_csv(basepath + '\\RFD_FooterrorP020B.csv', sep = ';')#create a csv file