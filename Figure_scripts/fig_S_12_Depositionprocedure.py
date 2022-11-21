# =============================================================================
# Checking the importance of Perovskite_deposition_procedure for the Jsc/Jqe value
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
            'Perovskite_composition_short_form',
            'Ref_publication_date',
            'EQE_measured',
            'EQE_integrated_Jsc',
             'Perovskite_deposition_procedure',
        ] 

# pick out the columns to use
data = data[dataColumnsToUse()]

# Drop measurements at high and low light intensities
data = data[(data['JV_light_intensity'] > 90) & (data['JV_light_intensity'] < 110)]

# Drop all points where we do not have EQE data measured
data = data[data['EQE_measured'] == True]

# Create a column for Jsc/Jqe
data['Jsc_over_Jqe'] = data['JV_default_Jsc']/data['EQE_integrated_Jsc']

# Filter out the most common HTL
antal = 10
common_procedures = data['Perovskite_deposition_procedure'].value_counts().index.tolist()[0:antal] 

data2 = data[data['Perovskite_deposition_procedure'].isin(common_procedures)]

#%% Setting up figure boxplot #############################################################
fileName = 'Jsc_over_Jqe_deposition_boxplot_version_2'

sns.set_style("darkgrid") # Set the graphical theme
fig = plt.figure(figsize=(8, 8), tight_layout=True) # Set up a figure

# Boxplot
ax = sns.boxplot(x="Perovskite_deposition_procedure", y="Jsc_over_Jqe", data=data2, order = common_procedures)

# line
ax.plot([-0.5, 9.5], [1, 1] , linewidth=2, color = 'black', alpha = 0.7)

ax.set_yticks(np.arange(0, 30, step = 0.1))
ax.set_ylim(0.6, 1.4)
ax.set_ylabel(r"$J_{sc,JV}/J_{sc,EQE}\,$")

#ax.set_xlim(0, end)
#ax.set_xticklabels(ax.get_xticklabels(),rotation=90)
ax.set_xlabel("")
ax.set(xticklabels=np.arange(1, 11, step = 1).tolist())

ax.set_title('Impact of perovsktie deposition', fontsize = 25, loc = 'center')

UtilityFunctions.axessetting(ax, fontsize = 30)

plt.show()
# UtilityFunctions.saveFigure(path_figure_folder = path_figure_folder, fileName = fileName)


#%% Get mean values for the most common hole conductors
common_procedures
Number_of_counts = data2['Perovskite_deposition_procedure'].value_counts()
median_values = data2.groupby('Perovskite_deposition_procedure').median() 



