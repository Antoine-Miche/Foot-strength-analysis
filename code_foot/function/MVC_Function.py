# -*- coding: utf-8 -*-
"""
Created on Sat Mar  5 17:55:42 2022

@author: Antoine MICHEL
@description : function to analyze the maximal strength of each componant of the strength with graphical interaction
@return : MVC_DataFrame

"""
"""
import pandas as pd
MVC_DataFrame = pd.DataFrame(columns = ['Contraction_number', 'check','ID', 'Contraction_type', 'Session','foot','FMAXz', 
                'TimeMVCz','FMAXy','TimeMVCy', 'FMAXx', 'TimeMVCx', 'FMAXzy','TimeMVCzy', 
                'FMAXxyz','TimeMVCxyz'])
For_RFD =[]

from function.MVC_Function import MVC

MVC_For_RFD =[] #initialisation of a list wich take into account the MVC with the Max-Min like during the data acquisition
MVC(MVC_File, MVC_DataFrame, resultantlist[increment],MVC_For_RFD,fe)  #run the MVC analysis  see function MVC
MVC_For_RFD = max (MVC_For_RFD) #take the maximal MVC for the file to be use for the RFD analysis
For_RFD.append(MVC_For_RFD) # add MVC for another list of MVC
plt.close('all') #close all the plot

"""
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import Button
from function.time_function import time
from function.Baseline_function import baseline


def MVC (resultant, MVC_DataFrame, resultantlist, MVC_For_RFD, fe):
    
    #change the time for the resultant list
    resultant = time (resultant, fe)
    
    around = 50#initialisation de variable to take 50 points before and after for the mean 0,05sif fe = 1000
    
    #find the number of zeros to split each contraction
    number_MVC = np.where (resultant[0] == 0)
    
    #loop for each MVC with the 0
    for ii in range(1,len(number_MVC[0])-1):
        
        #initialisation of different list to calculate the mean of each componant of the strength
        calz = []
        caly =[]
        calx =[]
        calzy = []
        calxyz =[]
        
        #create a class for the button on the graph with two possibilities good or strange
        class MVC :
            option = ''
        def OK(test):
            MVC.option = 'good'
            plt.close()
        def CM(test):
            MVC.option = 'Strange'
            plt.close()
        
        #create a plot with the two bouttons with only Fz
        fig = plt.figure()
        ax = fig.subplots()
        plt.subplots_adjust( bottom = 0.25)
        p,=ax.plot(resultant [1][number_MVC[0][ii-1]:number_MVC[0][ii]],color="blue")
        
        #create the two buttons
        axprev = plt.axes([0.8, 0.05, 0.1, 0.075])
        strange = Button(axprev, 'Strange',color="yellow")

        axnext = plt.axes([0.65, 0.05, 0.1, 0.075])
        Good= Button(axnext, 'OK',color="yellow")
        
        #change the value of the class good or strange
        strange.on_clicked(CM)
        Good.on_clicked(OK)
        
        #stop the code 5 seconds it's the time for the graphical interaction // maybe it can be interesting to change it
        plt.pause(5)
        
        #plot for the analysis with all the component of the strength
        plt.figure ()
        plt.plot(resultant[1][number_MVC[0][ii-1]:number_MVC[0][ii]])
        plt.plot (resultant[2][number_MVC[0][ii-1]:number_MVC[0][ii]])
        plt.plot (resultant[3][number_MVC[0][ii-1]:number_MVC[0][ii]])
        plt.plot (resultant[4][number_MVC[0][ii-1]:number_MVC[0][ii]])
        plt.plot (resultant[5][number_MVC[0][ii-1]:number_MVC[0][ii]])
        
        #graphical interaction 4 points the two first for the baseline and the two other to do the rolling average
        points = plt.ginput(4)
        plt.close()
        
        #initialisation of each variable we use int because float was forbidden for slicing
        baseline1 = int(points[0][0])
        baseline2 = int(points[1][0])
        onset = int(points[2][0])
        end = int(points[3][0])
        
        #loop for rolling average
        for i in range (len(resultant [0][onset:end])) :
            #Fmaxz and time to peak
            calz.insert (i,np.mean(resultant[1][onset+i-around : onset+around+i]))
            MAXz = max(calz)
            #Fmaxy and time to peak
            caly.insert (i,np.mean(resultant[2][onset+i-around : onset+around+i]))
            MAXy = max(caly)
            #Fmaxx and time to peak
            calx.insert (i,abs(np.mean(resultant[3][onset+i-around : onset+around+i])))
            MAXx = max (calx)
            #Fmaxzy and time to peak
            calzy.insert(i,np.mean(resultant[4][onset+i-around : onset+around+i]))
            MAXzy = max (calzy)
            #Fmaxxyz and time to peak
            calxyz.insert(i,np.mean(resultant[5][onset+i-around : onset+around+i]))
            MAXxyz = max(calxyz)
        
        # Max - Baseline for each componantof the strength
        FMAXz = MAXz - baseline(resultant[1][baseline1:baseline2])
        MVC_For_RFD.append(FMAXz)
        FMAXy = MAXy - baseline(resultant[2][baseline1:baseline2])
        FMAXx = MAXx - baseline(abs(resultant[3][baseline1:baseline2]))
        FMAXzy = MAXzy - baseline(resultant[4][baseline1:baseline2])
        FMAXxyz = MAXxyz - baseline(resultant[5][baseline1:baseline2])
        
        # time to peak of each componentof the strength
        TimeMVCz = resultant[0][calz.index(MAXz)+onset]
        TimeMVCy =  resultant[0][caly.index(MAXy)+onset]
        TimeMVCx =  resultant[0][calx.index(MAXx)+onset]
        TimeMVCzy= resultant[0][calzy.index(MAXzy)+onset]
        TimeMVCxyz = resultant[0][calxyz.index(MAXxyz)+onset]
        
        #Visual check of the max for each componant of the strength
        plt.figure()
        plt.plot(resultant[0][number_MVC[0][ii-1]:end],resultant[1][number_MVC[0][ii-1]:end])
        plt.plot (resultant[0][number_MVC[0][ii-1]:end],resultant[2][number_MVC[0][ii-1]:end])
        plt.plot (resultant[0][number_MVC[0][ii-1]:end],resultant[3][number_MVC[0][ii-1]:end])
        plt.plot (resultant[0][number_MVC[0][ii-1]:end],resultant[4][number_MVC[0][ii-1]:end])
        plt.plot (resultant[0][number_MVC[0][ii-1]:end],resultant[5][number_MVC[0][ii-1]:end])
        
        plt.legend(['Fz','Fy','Fx','Fzy','Fzyx'])
        plt.plot(TimeMVCz,resultant[1][calz.index(MAXz)+onset],'or')
        plt.plot (TimeMVCy,resultant[2][caly.index(MAXy)+onset],'or')
        plt.plot (TimeMVCx,resultant[3][calx.index(MAXx)+onset],'or')
        plt.plot (TimeMVCzy,resultant[4][calzy.index(MAXzy)+onset],'or')
        plt.plot (TimeMVCxyz,resultant[5][calxyz.index(MAXxyz)+onset],'or')
        plt.xlabel("Time (s)", size = 14)
        plt.ylabel("Force (N)", size = 14)
        plt.title("Example for MVC analysis", fontdict = {'size':16})
        
        
        #all the variable are put directly in the MVC Dataframe
        MVC_DataFrame.loc[len(MVC_DataFrame)] = [ii,MVC.option,resultantlist[0], 'MVC', resultantlist[3],resultantlist[1], FMAXz, 
                TimeMVCz,FMAXy,TimeMVCy, FMAXx, TimeMVCx, FMAXzy,TimeMVCzy, 
                FMAXxyz,TimeMVCxyz]
        
        
    return MVC_DataFrame