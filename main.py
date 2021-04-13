from scipy import stats
from scipy.stats import iqr
import numpy as np
import pandas as pd

df = pd.read_csv('wellbore_data_producer_wells.csv')

class Well:
    #
    #   __init()__ function for Well
    #
    #   description: takes the individual column value for the row being evaluated and puts this data into the Well object
    # 

    def __init__(self, well):
        x = well['X, m']
        y = well['Y, m']
        depth = well['Depth, m']
        if (well['Porosity, fraction'] != None):
            poros = well['Porosity, fraction'] 
        else:
            # imputation function GOES HERE
            poros = 0
        if (well['Permiability, mD'] != None):
            permiablity = well['Permiability, mD']
        else: 
            # imputation function GOES HERE
            permiablity = 0
        
        ai = well['Accoustic Impedance, kg*s/m^2']

        rock = well['Rock facies']

data_floats = df.select_dtypes(include=[np.float64])

#   FUNCTION flag_outliers( DataFrame )
#   
#   description: this function is used to calculate the outliers in our data sets based upon the iqr
#
def flag_outliers(data):
    outliers = []
    #   the function begins by taking the columns that have float values and iterating them one whole column at a time
    for col in data:
        #   this variable holds the column index 
        x = df.columns.get_loc(col)

        print(data[col].tolist())
        #   lower and upper are set to the threshold of where we would consider our data to be outlying
        lower, upper = outlier_treatment(data[col].tolist())
        
        # print(x, (upper, lower), data[col].tolist())
        for y in range(0, len(data[col])):
            if (data[col][y] > upper or data[col][y] < lower):
                outliers.append((x, y))
    return outliers

def outlier_treatment(data_col):
    data_col = sorted(data_col)
    q1, q3 = np.percentile(data_col, [25, 75])
    iqr = q3 - q1
    lower_range = q1 - (1.5 * iqr)
    upper_range = q3 + (1.5 * iqr)

    return lower_range, upper_range

print(flag_outliers(data_floats))
