# -*- coding: utf-8 -*-
"""
Created on Sat Mar  5 17:57:20 2022

@author: Antoine MICHEL
@description : Take the file directly in the folder and put the value in a list with the partipant ID, foot, and session
@return : data
example:
    
import os as os
from function.wrapper_function import wrapper
basepath = '..\code_foot'
fileList = os.listdir('..\code_foot')
data = wrapper (basepath,fileList)


"""
import pandas as pd
import os as os
import re


def wrapper (basePath,fileList) :
    """récupère les fichiers directement dans les fichiers et les mets dans une liste avec le nom"""
    list1 = []

    fileExt = r".txt"
    fichier = [_ for _ in os.listdir(basePath) if _.endswith(fileExt)]
    for ii in range (len(fichier)):
        """split the name """
        participantID = re.split("[._]",fichier[ii])[0] #ID
        date = re.split("[_]",fichier[ii])[1] #DATE
        pieds = re.split("[_]",fichier[ii])[2] #Right or left
        session = re.split("[._]",fichier[ii])[-2] #S1, S2, S3 or S4
        typeContract = re.split("[._]",fichier[ii])[-3] #MVC or RFD
        os.chdir(basePath)
        data = pd.read_csv(fichier[ii], sep = "\t" ,encoding='cp1252',names = ['time', 'CH1','CH2','CH3','CH4','CH5','CH6', 'Fz', 'Fx', 'Fy', 'comments'], decimal = ',', low_memory=False) #open the txt data
        DataUse = [participantID,pieds,date,session,typeContract,data] #list of data brut
        list1.append (DataUse) #add data brut for each participants in a list for treatment
    return list1