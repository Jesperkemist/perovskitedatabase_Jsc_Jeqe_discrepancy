# =============================================================================
# Ploting EQE vs Jsc
# 
# By Jesper Jacobsson
# 2021 12
# =============================================================================

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

# Sort out measurements at high and low light intensities
data = data[(data['JV_light_intensity'] > 90) & (data['JV_light_intensity'] < 110)]

# drop all points where we do not have EQE data measured
data = data[data['EQE_measured'] == True]

# Keep only certified data
data = data[data['JV_certified_values'] == True]


#%% Setting up figure PCE #############################################################
fileName = 'Jsc_vs_Jqe_version_3'

sns.set_style("darkgrid") # Set the graphical theme
fig = plt.figure(figsize=(8, 8), tight_layout=True) # Set up a figure

# Scatterplot
ax = sns.scatterplot(data=data, 
                     x="JV_default_Jsc", 
                     y="EQE_integrated_Jsc",
                     color = "blueviolet",
                     alpha = 0.3,
                     s = 25)

# line
ax.plot([0, 40], [0, 40] , linewidth=2, color = 'black', alpha = 0.7)


ax.set_ylim(0, 30)
ax.set_yticks(np.arange(0, 30, step = 3))
ax.set_ylabel(r"$J_{sc,EQE}\, [mA/cm^2]$")

ax.set_xlabel(r"$J_{sc,JV}\, [mA/cm^2]$")
ax.set_xticks(np.arange(0, 30, step = 3))
ax.set_xlim(0, 30)

ax.set_title('$J_{sc,EQE}\ vs\ J_{sc,JV}$', fontsize = 25, loc = 'center')

UtilityFunctions.axessetting(ax, fontsize = 30)


plt.show()
#  UtilityFunctions.saveFigure(path_figure_folder = path_figure_folder, fileName = fileName)

