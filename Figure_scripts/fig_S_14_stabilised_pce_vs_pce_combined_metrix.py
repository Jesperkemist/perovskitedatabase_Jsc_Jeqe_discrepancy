# =============================================================================
# Comparing PCE and stabilised PCE with Jsc/Jeqe values
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
            'Stabilised_performance_measured',
            'Stabilised_performance_procedure',
            'Stabilised_performance_PCE',
            'Stabilised_performance_Vmp',
            'Stabilised_performance_Jmp',
            'JV_reverse_scan_Voc',
            'JV_reverse_scan_Jsc',
            'JV_reverse_scan_FF',
            'JV_reverse_scan_PCE',
            'JV_reverse_scan_Vmp',
            'JV_reverse_scan_Jmp',
            'EQE_measured',
            'EQE_integrated_Jsc',
        ] 

# Ensure that all publication dates are in the right format
data['Ref_publication_date'] = UtilityFunctions.convertToDatetime(data['Ref_publication_date'])

# pick out the columns to use
data = data[dataColumnsToUse()]

# Drop measurements at high and low light intensities
data = data[(data['JV_light_intensity'] > 90) & (data['JV_light_intensity'] < 110)]

# Drop all points where we do not have stabilised PCE
data = data[data['Stabilised_performance_measured'] == True]

# Create a column for PCEsc_over_PCEstab
data['PCEsc_over_PCEstab'] = data['JV_reverse_scan_PCE']/data['Stabilised_performance_PCE']

## Drop all points where we do not have EQE data measured
data = data[data['EQE_measured'] == True]

# Create a column for Jsc/Jqe
data['Jsc_over_Jqe'] = data['JV_default_Jsc']/data['EQE_integrated_Jsc']

# Comparing the two comparisons
data['Jsc_over_Jqe_vs_PCEsc_over_PCEstab'] = data['Jsc_over_Jqe']/data['PCEsc_over_PCEstab']


#%% Setting up figure PCE #############################################################
fileName = 'Jsc_over_Jqe_vs_PCEsc_over_PCEstab_scatterplot_version_1'

sns.set_style("darkgrid") # Set the graphical theme
fig = plt.figure(figsize=(8, 8), tight_layout=True) # Set up a figure

# Scatterplot
ax = sns.scatterplot(data=data, 
                     x="Jsc_over_Jqe", 
                     y="PCEsc_over_PCEstab",
                     color = "forestgreen",
                     alpha = 0.3,
                     s = 25)

# line
ax.plot([1, 1], [0, 2] , linewidth=2, color = 'black', alpha = 0.7)
ax.plot([0, 2], [1, 1] , linewidth=2, color = 'black', alpha = 0.7)



ax.set_yticks(np.arange(0, 2, step = 0.05))
ax.set_ylabel(r"$PCE_{JV}/PCE_{stab}$")
ax.set_ylim(0.9, 1.15)

ax.set_xlabel(r"$J_{sc,JV}/J_{sc,EQE}$")
ax.set_xticks(np.arange(0, 2, step = 0.05))
ax.set_xlim(0.9, 1.15)

#ax.set_title('$J_{sc,EQE}\ vs\ J_{sc,JV}$', fontsize = 25, loc = 'center')

UtilityFunctions.axessetting(ax, fontsize = 30)


plt.show()
# UtilityFunctions.saveFigure(path_figure_folder = path_figure_folder, fileName = fileName)



#%% Setting up a histogram plot #############################################################
fileName = 'Jsc_over_Jqe_vs_PCEsc_over_PCEstab_histogram_version_1'

sns.set_style("darkgrid") # Set the graphical theme
fig = plt.figure(figsize=(8, 8), tight_layout=True) # Set up a figure

# barplot
binwidth = 0.004
ax = sns.histplot(data=data, x="Jsc_over_Jqe_vs_PCEsc_over_PCEstab", kde=False, binwidth=binwidth, color = 'forestgreen', alpha = 1)

# line
ax.plot([1, 1], [0, 1000] , linewidth=2, color = 'black', alpha = 1)


ax.set_xlabel(r"$(J_{sc,JV}/J_{sc,EQE})/(PCE_{JV}/PCE_{stab})$")
ax.set_ylabel(r"$Counts$")
ax.set_xlim(0.8, 1.3)
ax.set_ylim(0, 75)

#ax.set_title('$J_{sc,JV}/J_{sc,EQE}\ distribution$', fontsize = 25, loc = 'center')

UtilityFunctions.axessetting(ax, fontsize = 30)

plt.show()
# UtilityFunctions.saveFigure(path_figure_folder = path_figure_folder, fileName = fileName)



# calculating statistics
data.replace([np.inf, -np.inf], np.nan, inplace=True)
data.dropna(subset = ['Jsc_over_Jqe_vs_PCEsc_over_PCEstab'], inplace = True)
# 1706 datapoints

data['Jsc_over_Jqe_vs_PCEsc_over_PCEstab'].median()
data['Jsc_over_Jqe_vs_PCEsc_over_PCEstab'].mean()
data['Jsc_over_Jqe_vs_PCEsc_over_PCEstab'].std()

#data['Jsc_over_Jqe_vs_PCEsc_over_PCEstab'].median()
#1.0163453298820548
#data['Jsc_over_Jqe_vs_PCEsc_over_PCEstab'].mean()
#1.0389545139501202
#data['Jsc_over_Jqe_vs_PCEsc_over_PCEstab'].std()
#0.3048134346375889

# Remove large and small values
data = data[data['Jsc_over_Jqe_vs_PCEsc_over_PCEstab'] > 0.8]
data = data[data['Jsc_over_Jqe_vs_PCEsc_over_PCEstab'] < 1.2]
# 1600 datapoints remain

#data['Jsc_over_Jqe_vs_PCEsc_over_PCEstab'].median()
#1.0145475436712799
#data['Jsc_over_Jqe_vs_PCEsc_over_PCEstab'].mean()
#1.0161224074809525
#data['Jsc_over_Jqe_vs_PCEsc_over_PCEstab'].std()
#0.061492767443822725