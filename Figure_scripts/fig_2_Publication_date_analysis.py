# =============================================================================
# Checking the importance of Hysteresis for the Jsc/Jqe value
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

# Drop measurements at high and low light intensities
data = data[(data['JV_light_intensity'] > 90) & (data['JV_light_intensity'] < 110)]

# Drop all points where we do not have EQE data measured
data = data[data['EQE_measured'] == True]

# Create a column for Jsc/Jqe
data['Jsc_over_Jqe'] = data['JV_default_Jsc']/data['EQE_integrated_Jsc']

#%% Setting up figure boxplot #############################################################
fileName = 'Jsc_over_Jqe_date_boxplot_version_3'

# Bin the data with respect to Voc
start = datetime.date(2013, 1, 1)
end = datetime.date(2021, 1, 1)
#delta = 0.05
#antal = int(round((end-start)/delta)) + 1

bins_dt = pd.date_range('2013-06-01', freq='6M', periods=16)
bins_str = bins_dt.astype(str).values
labels = ['({}, {}]'.format(bins_str[i-1], bins_str[i]) for i in range(1, len(bins_str))]
#labels = np.linspace(1, 16, 16)

data['bin'] = pd.cut(data['Ref_publication_date'].astype(np.int64)//10**9,
                   bins=bins_dt.astype(np.int64)//10**9,
                   labels=labels)

#cut_bins = np.linspace(start, end, antal)
#cut_labels = np.linspace(start+delta/2, end + delta/2, antal)[:-1]

#data['bin'] = pd.cut(data['Ref_publication_date'], bins=cut_bins, labels=cut_labels)
#data['bin'] = pd.cut(data['Ref_publication_date'], bins=cut_bins)

sns.set_style("darkgrid") # Set the graphical theme
fig = plt.figure(figsize=(8, 8), tight_layout=True) # Set up a figure

# Boxplot
ax = sns.boxplot(x="bin", y="Jsc_over_Jqe", data=data)

# line
ax.plot([-0.5, 14.5], [1, 1] , linewidth=2, color = 'black', alpha = 0.7)

ax.set_yticks(np.arange(0, 30, step = 0.1))
ax.set_ylim(0.6, 1.4)
ax.set_ylabel(r"$J_{sc,JV}/J_{sc,EQE}$")

#ax.set_xlim(0, end)
#ax.set_xticklabels(ax.get_xticklabels(),rotation=90)
ax.set_xlabel(r"$Publication\, date$")
#a = [Text(0, 0, '(2999]'), Text(1, 0, '(2013-12-31, 2014-06-30]'), Text(2, 0, '(2014-06-30, 2014-12-31]'), Text(3, 0, '(2014-12-31, 2015-06-30]'), Text(4, 0, '(2015-06-30, 2015-12-31]'), Text(5, 0, '(2015-12-31, 2016-06-30]'), Text(6, 0, '(2016-06-30, 2016-12-31]'), Text(7, 0, '(2016-12-31, 2017-06-30]'), Text(8, 0, '(2017-06-30, 2017-12-31]'), Text(9, 0, '(2017-12-31, 2018-06-30]'), Text(10, 0, '(2018-06-30, 2018-12-31]'), Text(11, 0, '(2018-12-31, 2019-06-30]'), Text(12, 0, '(2019-06-30, 2019-12-31]'), Text(13, 0, '(2019-12-31, 2020-06-30]'), Text(14, 0, '(2020-06-30, 2020-12-31]')]

a = ['','2014','','','','2016','','','','2018','','','','2020','']
ax.set(xticklabels=a)

ax.set_title('$Impact\, of\, publication\, date$', fontsize = 25, loc = 'center')

UtilityFunctions.axessetting(ax, fontsize = 30)

plt.show()
# UtilityFunctions.saveFigure(path_figure_folder = path_figure_folder, fileName = fileName)


#%% Setting up figure scatterplot #############################################################
fileName = 'Jsc_over_Jqe_date_version_2'

sns.set_style("darkgrid") # Set the graphical theme
fig = plt.figure(figsize=(8, 8), tight_layout=True) # Set up a figure

# Scatterplot
ax = sns.scatterplot(data=data, 
                     x="Ref_publication_date", 
                     y="Jsc_over_Jqe",
                     color = "blueviolet",
                     alpha = 0.5,
                     s = 20)

# line
ax.plot([datetime.date(2013, 1, 1), datetime.date(2021, 1, 1)], [1, 1] , linewidth=2, color = 'black', alpha = 0.7)


ax.set_yticks(np.arange(0, 2, step = 0.1))
ax.set_ylabel(r"$J_{sc,JV}/J_{sc,EQE}$")
ax.set_ylim(0.6, 1.4)

ax.set_xlabel(r"$Publication\, date$")
ax.set_xticks(np.arange(0, 30, step = 0.2))
ax.set_xlim(0.6, 1.4)

ax.xaxis_date()
ax.set_xticks([datetime.date(2014, 1, 1), datetime.date(2016, 1, 1), datetime.date(2018, 1, 1), datetime.date(2020, 1, 1)])
ax.xaxis.major.formatter.scaled[1.0] = "%Y"
ax.set_xlim(datetime.date(2013, 1, 1), datetime.date(2021, 1, 1))

ax.set_title('$Impact\, of\, publication\, date$', fontsize = 25, loc = 'center')

UtilityFunctions.axessetting(ax, fontsize = 30)

plt.show()
# UtilityFunctions.saveFigure(path_figure_folder = path_figure_folder, fileName = fileName)

