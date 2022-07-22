# -*- coding: utf-8 -*-
"""
Created on Sat Mar  5 17:55:43 2022

@author: Antoine MICHEl
@description : function to analyze the rate of force devlopment of Fz, Fzy, Fzyx componant of the strength with 
graphical interaction
@return : RFD_error dataFrame and RFD_DataFrame


to test this function use the variables in the file : Variables_to_import ==> Test_Function

RFD(RFD_File, MVC_For_RFD,resultantlist[i],fe,listerror_RFD,RFD_Value)


"""
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import Button
from function.time_function import time
from function.Baseline_function import baseline


def RFD (RFD_File, MVC,resultantlist, fe, listerror_RFD, RFD_Value):
    
    #select only the column that we use for a loop see after
    res_Z= [1,4,5]
    
    #list of the value for the RFD if the fe = 1000Hz change it if the fe was different
    valimp = [50,100,200,250]
    
    #change the time for the resultant list
    time(RFD_File,fe)
    
    #find the number of zeros to split each contraction
    number_RFD = np.where (RFD_File[0] == 0)
    
    #loop for each RFD with the 0
    for ii in range(1,len(number_RFD[0])):
        
        #search the comment to see if heel raise
        Heelr = np.where(resultantlist[-1][number_RFD[0][ii-1]:number_RFD[0][ii]].str.contains('#7 hp') == True)#double check
        
        #search the comment if Knee pushing
        KneeP = np.where(resultantlist[-1][number_RFD[0][ii-1]:number_RFD[0][ii]].str.contains('#7 kp') == True)#double check 
        
        #add an error if heel raise and pass on the next contraction
        if len(Heelr[0]) == 1:
            listerror_RFD.append([ii,resultantlist[0], 'error, heel raise', resultantlist[1],resultantlist[3]])
        
        #add an error if heel raise and pass on the next contraction
        elif len(KneeP[0]) == 1:
            listerror_RFD.append([ii,resultantlist[0], 'error, KP', resultantlist[1],resultantlist[3]])
        
        #else begin other check with the graph
        else:
            
            #define the seuil
            seuil = 0.2
    
            #create a plot   
            plt.close()
            plt.plot (RFD_File[1][number_RFD[0][ii-1]:number_RFD[0][ii]])
            plt.title('3 point')
            
            #interaction with only one point to find the onset manually first time to exvclude or include the contraction
            #only for the Fz because the check during the acquisition was only on Fz
            points = plt.ginput(3)
            plt.close ()
            
            un = int(points[0][0])
            deux = int(points[1][0])
            sdman = RFD_File[1][un:deux].std()
            meanman = RFD_File[1][un:deux].mean()
            
            
            #create a class and function for graphic interaction
            class valeur :
                val = 0
            def OK(test):
                valeur.val = 1
                plt.close()
            def CM(test):
                valeur.val=2
                plt.close()
            def PreTension(test):
                valeur.val=3
                plt.close()
            
            #plot the contraction with button only for Fz
            fig = plt.figure()
            ax = fig.subplots()

            plt.subplots_adjust( bottom = 0.25)
            p,=ax.plot(RFD_File [1][number_RFD[0][ii-1]:number_RFD[0][ii]],color="blue")

            ax.plot()

            ax.axhline(meanman + 3*sdman, color='gray', linestyle='--')
            ax.axhline(meanman + 5*sdman, color='red', linestyle='--')
            ax.axhline(meanman - 3*sdman, color='gray', linestyle='--')
            ax.axhline(meanman - 5*sdman, color='red', linestyle='--')
            
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
            CMov.on_clicked(CM)
            Good.on_clicked(OK)
            
            #pause to have the time for the interaction
            plt.pause(5)
            
            #if the class == 2 put an error with the reason
            if valeur.val == 2:
                listerror_RFD.append([ii,resultantlist[0], 'error CM', resultantlist[1],resultantlist[3]])
            
            #if the class == 3 put an error with the reason
            elif valeur.val == 3:
                listerror_RFD.append([ii,resultantlist[0], 'error Pretension', resultantlist[1],resultantlist[3]])
            
            #if the value was 1 do other check
            elif valeur.val == 1:
                
               
                
                #find the max and the indice of the max of the rfd useful for the check after
                maxZ = max (RFD_File[1][number_RFD[0][ii-1]:number_RFD[0][ii]])
                ind_max = np.where(RFD_File[1]==maxZ)
                ind_max = ind_max[0][0]
                
                #if the index of max-onset was > 1 error in list
                if RFD_File[0][ind_max]-RFD_File[0][int(points[0][0])] < seuil or RFD_File[0][ind_max]-RFD_File[0][int(points[0][0])]>1:
                    listerror_RFD.append([ii,resultantlist[0], 'error time', resultantlist[1],resultantlist[3]])
                    
                #if the Fmax was < 70% to the MVC put an error
                elif max(RFD_File[1][number_RFD[0][ii-1]:number_RFD[0][ii]])-min(RFD_File[1][number_RFD[0][ii-1]:int(points[0][0])]) < MVC*0.7 :
                    listerror_RFD.append([ii,resultantlist[0], 'error < 70%', resultantlist[1],resultantlist[3]])
                    
                #if the Fmax was > MVC put an error
                elif max(RFD_File[1][number_RFD[0][ii-1]:number_RFD[0][ii]])-min(RFD_File[1][number_RFD[0][ii-1]:int(points[0][0])]) > MVC :
                    listerror_RFD.append([ii,resultantlist[0], 'error > MVC', resultantlist[1],resultantlist[3]])
                
                #else run the analysis
                else:
                    #create a list for the rfd
                    list_RFD = []
                    
                    #add some information in the list
                    list_RFD.append(ii+1)#number of contraction
                    list_RFD.append(resultantlist[0])#ID
                    list_RFD.append('RFD')
                    list_RFD.append(resultantlist[3])#session
                    list_RFD.append(resultantlist[1])#right or left
                    
                    #run the analysis for the three componant of the force Fz FZY FXYZ
                    for col in res_Z:
                        
                        #create plot for the interaction
                        plt.close()
                        plt.plot (RFD_File[col][number_RFD[0][ii-1]:number_RFD[0][ii]])
                        plt.title('3 points')
                        
                        #graphical interaction
                        points = plt.ginput(3)# onset for each columns of the strength
                        plt.close ()
                        manualonset = int(points[2][0])
                        
                        #add the manual onset in the list
                        list_RFD.append(manualonset)
                        
                        #add the autoonset in the list

                        list_RFD.append((maxZ-baseline(RFD_File[col][int(points[0][0]):int(points[1][0])]))/MVC*100)
                        
                        #plot the two onset on a graph to have a control visually
                        plt.plot (RFD_File[col][number_RFD[0][ii-1]:number_RFD[0][ii]])
                        plt.xlabel("Time (s)", size = 14)
                        plt.ylabel("Force (N)", size = 14)
                        plt.title("Example for RFD analysis", fontdict = {'size':16})
                        plt.legend(['Fz'])
                        plt.plot (manualonset,RFD_File[col][manualonset], 'o', c = 'green')
                        plt.plot (manualonset+50,RFD_File[col][manualonset+50], 'o', c = 'green')
                        plt.plot (manualonset+100,RFD_File[col][manualonset+100], 'o', c = 'green')
                        plt.plot (manualonset+200,RFD_File[col][manualonset+200], 'o', c = 'green')
                        plt.plot (manualonset+250,RFD_File[col][manualonset+250], 'o', c = 'green')
                        
                        #analysis of the rfd if the time xas >0.250
                        if RFD_File[0][ind_max]-RFD_File[0][int(points[0][0])] > 0.250:
                            if col== 1:
                                #in the list of control add that this contraction was good
                                listerror_RFD.append([ii,resultantlist[0], 'Good 250', resultantlist[1],resultantlist[3]])
                            for Imp in valimp:
                                list_RFD.append (np.trapz (RFD_File[col][manualonset:manualonset+Imp],dx = 0.001))#impulse with manual onset dx = 0.001 if the fe = 1000Hz add plot
                                slope, intercept = np.polyfit(RFD_File[0][manualonset:manualonset+Imp],RFD_File[col][manualonset:manualonset+Imp],1)
                                list_RFD.append(slope)#slope with manual onset

                            
                        else :
                            if col == 1 :
                                #in the list of control add that this contraction was good
                                listerror_RFD.append([ii,resultantlist[0], 'Good 200', resultantlist[1],resultantlist[3]])
                            
                            #analysis of the rfd if the time xas >0.200
                            for Imp in valimp:
                                if Imp == 250:
                                    #put 0 for 0.250
                                    list_RFD.append(None)
                                    list_RFD.append(None)
                                else : 
                                    list_RFD.append (np.trapz (RFD_File[col][manualonset:manualonset+Imp],dx = 0.001))#impulse manualonset
                                    slope, intercept = np.polyfit(RFD_File[0][manualonset:manualonset+Imp],RFD_File[col][manualonset:manualonset+Imp],1)
                                    list_RFD.append(slope)#slope manual onset

                            
                    RFD_Value.append(list_RFD)