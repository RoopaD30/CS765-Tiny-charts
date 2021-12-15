# -*- coding: utf-8 -*-
"""
Created on Sun Nov 14 14:28:32 2021

@author: roopa
"""


import matplotlib.pyplot as plt
import numpy as np
from matplotlib import colors
import pandas as pd
import os
import argparse
import sys

# =============================================================================
# # Creating dataset
# np.random.seed(23685752)
# N_points = 10000
# n_bins = 20
# 
# # Creating distribution
# x = np.random.randn(N_points)
# #y = .8 ** x + np.random.randn(10000) + 25
# =============================================================================


parser = argparse.ArgumentParser(description='Tiny Chart parser')
parser.add_argument('--infile', dest="infile", type=str, default="wnba.csv")
parser.add_argument('--column', dest="column", type=str,default="Weight")
parser.add_argument('--width', dest="width", type=float, default=5)
#parser.add_argument('--height', dest="height", type=int, default=5)
flags = parser.parse_args()


# Take the input file from user as first argument. The input file has to be in /data folder 
# from current working directory
dataset = pd.read_csv(os.path.join(os.getcwd(), 'data', flags.infile))

# Take the column name from user as second argument
column = flags.column

try:
    x = np.asarray(dataset[column])
    x = x[~pd.isnull(x)]
except Exception:
    print("The entered column is not present in the dataframe")
    sys.exit()


# Take the dimensions in inches from user as third and fourth arguments
d1 = flags.width
d2 = d1

if d1*d2 <= 2:
    plotHist = False
else:
    plotHist = True
    
if dataset[column].dtype != 'O':
    
    mode = dataset[column].skew(axis=0, skipna=True)

    if mode < -1 or mode > 1:
        print("Extremely Skewed")
        dist_type = "ESkewed"
    elif -1 < mode < -0.5 or 1 > mode > 0.5:
        print("Skewed")
        dist_type = "Skewed"
    elif mode < 0.5 or mode > -0.5:
        print("Symmetrical")
        dist_type = "Symmetrical"
    else:
        dist_type = "Default"
else:
    dist_type = "Ordinal"

if plotHist:
    
    if dist_type == "ESkewed":
        # Rice rule Gives more number of deviations. 
        # Suits Symmetrical -- Small dimensions 
        rice = int((len(dataset) ** (1/3)) * 2)
        n_bins = rice
    elif dist_type == "Skewed":
        # Scott's reference rule Optimal for the mid range dimensions chosen
        # Good for smaller dimensions tested
        scott = int(3.5 * np.nanstd(x) * (len(dataset) ** (-1/3)))
        n_bins = scott
    elif dist_type == "Symmetrical":
        Q1 = np.nanpercentile(x, 25, interpolation = 'midpoint')
    
        Q3 = np.nanpercentile(x, 75, interpolation = 'midpoint')
        
        IQR = Q3 - Q1
        
        # Freedman Diaconis Rule -- Might be better for smaller dimensions since lesser number of bins are being calculated
        # Good for small dimesions tested
        fred_dia = int(2 * IQR * (len(dataset) ** (-1/3)))
        n_bins = fred_dia
    else:
        # Rice rule Gives more number of deviations. 
        # Suits Symmetrical -- Small dimensions 
        rice = int((len(dataset) ** (1/3)) * 2)
        n_bins = rice

# =============================================================================
#     # PTS Skew
#     # Square of frequency Not suitable since color variation is not that much -- trsnalting to if the data variations being represented here are not optimal with colour
#     sq_freq = int(len(dataset)**0.5)
#     
#     # Sturges formula Almost same result as Square of frequency ; except for more number of bins and more variation is being shown
#     sturge = int(1 + (3.322 * np.log(len(dataset))))
# =============================================================================
    
    # Creating histogram
    fig, axs = plt.subplots(1, 1,
    						figsize = (d1, d2),
    						tight_layout = True)


    legend = ['distribution']
    
    # Remove axes splines
    for s in ['top', 'bottom', 'left', 'right']:
    	axs.spines[s].set_visible(False)
    
    # Add x, y gridlines
    axs.grid(b = True, color ='grey',
    		linestyle ='-.', linewidth = 0.5,
    		alpha = 0.6)
    
    # Creating histogram
    N, bins, patches = axs.hist(x, bins = n_bins)
    
    if dist_type != "ESkewed" and  dist_type != "Ordinal" and (d1 >2 or d2>2) :
        dataset[column].plot(kind='kde', ax=axs, secondary_y=True)
    
# =============================================================================
#     length = bins[len(bins)-1] - bins[0]
#     maxHeight = max(N)
#     area = sum(N) * length
#     
#     total_area = maxHeight * len(bins)-1
#     
#     percent = (area / total_area) * 100
#     print("Percentage of area occupied: ",percent)
# =============================================================================
    
    # Setting color
    fracs = ((N**(1 / 5)) / N.max())
    norm = colors.Normalize(fracs.min(), fracs.max())
    
    for thisfrac, thispatch in zip(fracs, patches):
     	color = plt.cm.viridis(norm(thisfrac))
     	thispatch.set_facecolor(color)
        
        
    if (dist_type == "ESkewed" and (d1 > 4 or d2 > 4)) or (dist_type != "ESkewed" and (d1 > 3 or d2 > 3)):
        labels = [int(i) for i in N]
      
        for rect, label in zip(patches, labels):
            height = rect.get_height()
            if height == 0:
                continue
            axs.text(round(rect.get_x() + rect.get_width() / 2), height+0.01, label,
                    ha='center', va='bottom')
    
    # Adding extra features
    plt.xlabel("X-axis")
    plt.ylabel("y-axis")
    # Show plot
    if d1 > 2 or d2 > 2:
        plt.title("Histogram for "+column)
    if d1 > 3 or d2 > 3:
        plt.legend(['Distribution'],bbox_to_anchor=(0.85,1.025), loc="upper left")
        
    if len(set(dataset[column])) > 20:
        plt.xticks([])
    elif len(set(dataset[column])) > 10:
        #plt.setp(axs.get_xticklabels(), rotation=30, horizontalalignment='right')
        plt.xticks(rotation=90)
    plt.show()
    #plt.savefig("output.png")

else:
    if dist_type != "Ordinal":
        dataset[column].plot.kde(figsize=(d1,d2))
        if d1 < 1:
            plt.axis('off')
        
        #plt.axis('off')
        plt.show()
        #plt.savefig("output.png")
    else:
        fig, axs = plt.subplots(1, 1,
    						figsize = (d1, d2),
    						tight_layout = True)
        axs.hist(x)
        plt.yticks([])
        plt.xticks([])
        if d1 < 1:
            plt.axis('off')
        plt.show()
        #plt.savefig("output.png")
