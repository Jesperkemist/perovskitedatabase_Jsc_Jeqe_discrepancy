# =============================================================================
# Calculating the standard distribution of the Jsc over Jqe data
# 
# By Jesper Jacobsson
# 2021 12
# =============================================================================

import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy.stats as st
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


#%% For the entire dataaset
mean = data['Jsc_over_Jqe'].mean()
std = data['Jsc_over_Jqe'].std()

#%% Removing outliers (somwhat arbitrarily defined as datapoints more than 25 % of a value of 1)
data2 = data[data['Jsc_over_Jqe'] > 0.75]
data2 = data2[data2['Jsc_over_Jqe'] < 1.25]

mean2 = data2['Jsc_over_Jqe'].mean()
std2 = data2['Jsc_over_Jqe'].std()

#%% Probabliity of measuring a value of Jqe belove Jsc
prob = st.norm.cdf( -((mean2-1)/std2) ) 



#%% Setting up figure PCE #############################################################
fileName = 'Jsc_over_Jqe_barplot_trimed_KDE_version_1'

#%% Plot
sns.set_style("darkgrid") # Set the graphical theme
fig = plt.figure(figsize=(8, 8), tight_layout=True) # Set up a figure

# barplot
binwidth = 0.004
ax = sns.histplot(data=data2, x="Jsc_over_Jqe", kde=True, binwidth=binwidth, color = 'darkorange', alpha = 1)

# line
ax.plot([1, 1], [0, 1000] , linewidth=2, color = 'black', alpha = 1)


ax.set_xlabel(r"$J_{sc}/J_{eqe}$")
ax.set_ylabel(r"$Counts$")
ax.set_xlim(0.75, 1.25)
ax.set_ylim(0, 250)

UtilityFunctions.axessetting(ax, fontsize = 30)

plt.show()
# UtilityFunctions.saveFigure(path_figure_folder = path_figure_folder, fileName = fileName)