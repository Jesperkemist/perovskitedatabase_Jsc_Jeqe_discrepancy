# =============================================================================
# Comparing PCE and stabilised PCE values
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

### Drop all points where we do not have EQE data measured
#data = data[data['EQE_measured'] == True]

## Create a column for Jsc/Jqe
#data['Jsc_over_Jqe'] = data['JV_default_Jsc']/data['EQE_integrated_Jsc']

## Comparing the two comparisons
#data['Jsc_over_Jqe_vs_PCEsc_over_PCEstab'] = data['Jsc_over_Jqe']/data['PCEsc_over_PCEstab']



#%% Setting up figure scatterplot #############################################################
fileName = 'PCE_vs_PCE_version_1'

sns.set_style("darkgrid") # Set the graphical theme
fig = plt.figure(figsize=(8, 8), tight_layout=True) # Set up a figure

# Scatterplot
ax = sns.scatterplot(data=data, 
                     x="JV_reverse_scan_PCE", 
                     y="Stabilised_performance_PCE",
                     color = "royalblue",
                     alpha = 0.3,
                     s = 25)

# line
ax.plot([0, 40], [0, 40] , linewidth=2, color = 'black', alpha = 0.7)


ax.set_ylim(0, 27)
ax.set_yticks(np.arange(0, 27, step = 3))
ax.set_ylabel(r"$PCE_{stab}\, [\%]$")

ax.set_xlabel(r"$PCE_{JV}\, [\%]$")
ax.set_xticks(np.arange(0, 27, step = 3))
ax.set_xlim(0, 27)

ax.set_title('$PCE_{stab}\ vs\ PCE_{JV}$', fontsize = 25, loc = 'center')

UtilityFunctions.axessetting(ax, fontsize = 30)


plt.show()
# UtilityFunctions.saveFigure(path_figure_folder = path_figure_folder, fileName = fileName)


#%% Setting up a histogram plot #############################################################
fileName = 'PCE_vs_PCE_histogram_version_1'

sns.set_style("darkgrid") # Set the graphical theme
fig = plt.figure(figsize=(8, 8), tight_layout=True) # Set up a figure

# barplot
binwidth = 0.004
ax = sns.histplot(data=data, x="PCEsc_over_PCEstab", kde=False, binwidth=binwidth, color = 'maroon', alpha = 1)

# line
ax.plot([1, 1], [0, 1000] , linewidth=2, color = 'black', alpha = 1)


ax.set_xlabel(r"$PCE_{JV}/PCE_{stab}$")
ax.set_ylabel(r"$Counts$")
ax.set_xlim(0.8, 1.3)
ax.set_ylim(0, 200)

#ax.set_title('$J_{sc,JV}/J_{sc,EQE}\ distribution$', fontsize = 25, loc = 'center')

UtilityFunctions.axessetting(ax, fontsize = 30)

plt.show()
# UtilityFunctions.saveFigure(path_figure_folder = path_figure_folder, fileName = fileName)



# calculating statistics
data.replace([np.inf, -np.inf], np.nan, inplace=True)
data.dropna(subset = ['PCEsc_over_PCEstab'], inplace = True)

#data['PCEsc_over_PCEstab'].std()
#1.8232793950380621
#data['PCEsc_over_PCEstab'].mean()
#1.1061469771520231
#data['PCEsc_over_PCEstab'].median()
#1.0235294117647058

# Notes
# 3369 datapoints has stabilised PCE