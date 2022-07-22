# -*- coding: utf-8 -*-
"""
Created on Tue Mar 29 11:14:17 2022

@author: antoi
"""
import matplotlib.pyplot as plt
from matplotlib.widgets import Button

def plot_button (RFD_File):
    class valeur :
        val = 0
    def OK(test):
        valeur.val = 1
        plt.close()
    def CM(test):
        valeur.val=2
        plt.close()
        return valeur.val
    def PreTension(test):
        valeur.val=3
        plt.close()
    
    #plot the contraction with button only for Fz
    fig = plt.figure()
    ax = fig.subplots()
    plt.subplots_adjust( bottom = 0.25)
    p,=ax.plot(RFD_File,color="blue")
    ax.plot()

    #create a button for the pretension
    axprev = plt.axes([0.8, 0.05, 0.1, 0.075])
    Pret = Button(axprev, 'PreT',color="yellow")

    #create a button for the contermovement
    axnext = plt.axes([0.65, 0.05, 0.1, 0.075])
    CMov = Button(axnext, 'CM',color="yellow")

    #create a button to tell if the contraction was good
    axes = plt.axes([0.5, 0.05, 0.1, 0.075])
    Good = Button(axes, 'OK',color="yellow")

    #give different value at the class 
    Pret.on_clicked(PreTension)
    valeur = CMov.on_clicked(CM)
    Good.on_clicked(OK)
    
    #pause to have the time for the interaction
    plt.pause(5)
    return valeur