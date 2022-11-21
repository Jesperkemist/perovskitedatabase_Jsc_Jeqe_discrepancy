# =============================================================================
# Checking the importance of PCE for the Jsc/Jqe value
# 
# By Jesper Jacobsson
# 2021 12
# =============================================================================
#%%
from dateutil.relativedelta import relativedelta
import datetime
import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

import UtilityFunctions

#%% File paths
fileName_data = 'Perovskite_database_content_all_data.csv'
cwd = os.path.abspath(os.getcwd())
top_directory = os.path.dirname(cwd)
path_raw_data = os.path.join(top_directory, "Data",)
path_figure_folder = os.path.join(top_directory, "Figures")
path_data = os.path.join(path_raw_data, fileName_data)


#%% Load data downloaded from the perovskite database
data = pd.read_csv(path_data, low_memory=False)

#%% Initial data manipulation
def dataColumnsToUse():
    ''' Returns a list of the data columns the app will use'''
    return [
            'Cell_area_measured',
            'JV_default_Voc',
            'JV_default_Jsc',
            'JV_default_FF',
            'JV_default_PCE',
            'JV_light_intensity',
            'JV_hysteresis_index',
            'JV_certified_values',
            'Perovskite_composition_short_form',
            'Ref_publication_date',
            'Stabilised_performance_PCE',
            'Stabilised_performance_Vmp',
            'Stabilised_performance_Jmp',
            'EQE_measured',
            'EQE_integrated_Jsc',
            'JV_reverse_scan_Voc',
            'JV_reverse_scan_Jsc',
            'JV_reverse_scan_FF',
            'JV_reverse_scan_PCE',
            'JV_reverse_scan_Vmp',
            'JV_reverse_scan_Jmp',
            'Perovskite_band_gap',
        ] 

# Ensure that all publication dates are in the right format
data['Ref_publication_date'] = UtilityFunctions.convertToDatetime(data['Ref_publication_date'])

# Convert the band gap column to numeric values (and keeping the first value if multiple values)
data['Perovskite_band_gap'] = UtilityFunctions.convertNumerListToFloats(data['Perovskite_band_gap'])

# pick out the columns to use
data = data[dataColumnsToUse()]

# Drop measurements at high and low light intensities
data = data[(data['JV_light_intensity'] > 90) & (data['JV_light_intensity'] < 110)]

# Drop all points where we do not have EQE data measured
data = data[data['EQE_measured'] == True]

# Create a column for Jsc/Jqe
data['Jsc_over_Jqe'] = data['JV_default_Jsc']/data['EQE_integrated_Jsc']


#%% Setting up figure scatterplot #############################################################
fileName = 'Jsc_over_Jqe_PCE_version_2'

sns.set_style("darkgrid") # Set the graphical theme
fig = plt.figure(figsize=(8, 8), tight_layout=True) # Set up a figure

# Scatterplot
ax = sns.scatterplot(data=data, 
                     x="JV_default_PCE", 
                     y="Jsc_over_Jqe",
                     color = "blueviolet",
                     alpha = 0.5,
                     s = 20)

# line
ax.plot([0, 35], [1, 1] , linewidth=2, color = 'black', alpha = 0.7)

ax.set_ylim(0, 2)
ax.set_yticks(np.arange(0, 2, step = 0.2))
ax.set_ylabel(r"$J_{sc,JV}/J_{sc,EQE}\,$")

ax.set_xlim(0, 27)
ax.set_xlabel(r"$PCE\, [\%]$")
ax.set_xticks(np.arange(0, 27, step = 3))

ax.set_title('Impact of PCE', fontsize = 25, loc = 'center')

UtilityFunctions.axessetting(ax, fontsize = 30)

plt.show()
# UtilityFunctions.saveFigure(path_figure_folder = path_figure_folder, fileName = fileName)


#%% Seting up figure boxplot #############################################################
fileName = 'Jsc_over_Jqe_PCE_boxplot_version_3'

# Bin the data with respect to PCE
start = 0.25
end = 23.25
delta = 1
antal = int(round((end-start)/delta)) + 1

cut_bins = np.linspace(start, end, antal)
cut_labels = np.linspace(start+delta/2, end + delta/2, antal)[:-1]

data['bin'] = pd.cut(data['JV_default_PCE'], bins=cut_bins, labels=cut_labels)

sns.set_style("darkgrid") # Set the graphical theme
fig = plt.figure(figsize=(8, 8), tight_layout=True) # Set up a figure

# Boxplot
ax = sns.boxplot(x="bin", y="Jsc_over_Jqe", data=data)

# line
ax.plot([-0.5, 22.5], [1, 1] , linewidth=2, color = 'black', alpha = 0.7)

ax.set_yticks(np.arange(0, 30, step = 0.1))
ax.set_ylim(0.6, 1.4)
ax.set_ylabel(r"$J_{sc,JV}/J_{sc,EQE}\,$")

#ax.set_xticklabels(ax.get_xticklabels(),rotation=90)
a = ['1', '', '3', '', '5', '', '7', '', '9', '', '11', '', '13', '', '15', '', '17', '', '19', '', '21', '', '23']
ax.set_xlabel(r"$PCE\, [\%]$")
ax.set(xticklabels=a)

ax.set_title('Impact of PCE', fontsize = 25, loc = 'center')

UtilityFunctions.axessetting(ax, fontsize = 30)

#plt.show()
UtilityFunctions.saveFigure(path_figure_folder = path_figure_folder, fileName = fileName)
