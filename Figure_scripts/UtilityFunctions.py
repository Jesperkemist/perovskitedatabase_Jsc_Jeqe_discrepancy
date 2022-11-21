# =============================================================================
# Utility functions
# 
# By Jesper Jacobsson
# 2021 12
# =============================================================================

import os
import datetime

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def axessetting(ax, fontsize = 16): 
    for item in ([ax.title, ax.xaxis.label, ax.yaxis.label] +
             ax.get_xticklabels() + ax.get_yticklabels()):
        item.set_fontsize(fontsize)

    return True

def convertToDatetime(data):
    '''Go trough data, which is assumed to be a pandas series, and convert all non datetime fields to 'NaT'''
    newData = []
    for i, time in enumerate(data):
        if isinstance(time, datetime.datetime) == False:
            try:
                newData.append(datetime.datetime.fromisoformat(time))
            except:
                newData.append(pd.to_datetime(''))
        else:
            newData.append(time)
    return newData

def convertNumerListToFloats(numberList):
    '''Convert a numerlist to floats. If more than one value, keep the first one'''

    # Convert data to strings
    numberList = numberList.astype(str)

    # identify all strings with more than one element, by utilizing that they contain the pattern ' | '
    x = numberList.str.contains(' | ') == True

    # Get a list of the indexes where the above condition holds
    indexlist = list(numberList[x].index)

    # Loop over all instances with more than one number
    for index in indexlist:
        # Ensure that entry is a string
        y = str(numberList[index]).strip()

        # Keep the first entry
        y = y.split(' | ')[0].strip()

        # Convert number into a float
        try:
            number = float(y)
        except:
            number = np.nan

        # Update data
        numberList.loc[index] = number

    # Convert everything to floats
    numberList = pd.to_numeric(numberList, errors = 'coerce')

    return numberList

def initialDataManipulation(data):
    '''Do initial data manipulation required by the app'''
    # Ensure that all publication dates are in the right format
    data['Ref_publication_date'] = convertToDatetime(data['Ref_publication_date'])

    # Convert the band gap column to numeric values (and keeping the first value if multiple values)
    data['Perovskite_band_gap'] = convertNumerListToFloats(data['Perovskite_band_gap'])

    return data

def saveFigure(path_figure_folder, fileName):
    plt.savefig(os.path.join(path_figure_folder, (fileName + '.tif')), dpi = 300, format = 'tif')
    plt.savefig(os.path.join(path_figure_folder, (fileName + '.png')), dpi = 300, format = 'png')
    plt.savefig(os.path.join(path_figure_folder, (fileName + '.pdf')), dpi = 300, format = 'pdf') 