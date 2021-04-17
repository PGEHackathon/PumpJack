from scipy import stats
from scipy.stats import iqr
import numpy as np
import pandas as pd
import math

class Well:
    #
    #   FUNCTION __init()__
    #
    #   description: takes the individual column value for the row being evaluated and puts this data into the Well object
    # 

    def __init__(self, well):
        #   id = well_no
        self.id = well['Well_ID'].unique()[0]
        #   x = unique x value (meters) in the 20 pieces of data
        self.x = well['X, m'].unique()[0]
        #   y = unique y value (meters) in the 20 pieces of data
        self.y = well['Y, m'].unique()[0]

        # self.attributes = []
        print(well)
        well = self.threshold_nan_filler(well)
        print(well)
        # for x in well.columns:
        #     self.attributes.append((x, list(well.loc[:, x].values)))

    def threshold_nan_filler(self, well):
        # create for loop to run through each column and return percent NaN 
        for column in well:
            missing_percent_stat = well[column].isnull().sum() * (1 / (len(well[column])))
            if (column == 'Rock facies'):
                continue
            elif (column == 'Well_ID' or column == 'X, m' or column == 'Y, m'):
                well = well.drop(column, 1)
            elif (missing_percent_stat >= .2):
                well = well.drop(column, 1)
            elif (missing_percent_stat <= .2):
                #   creating a masked array of data
                masked = np.ma.masked_array(well[column], np.isnan(well[column]))
                mean_filler = np.ma.average(masked)
                print(column, "with missing percent stat of:", missing_percent_stat, "\n with weighted column average of:", mean_filler)
                for i in range(len(well[column])):
                    print(well[column].iloc[i], "\t is nan:", math.isnan(well.at[i, column]))
                    if math.isnan(well.at[i, column]):
                        well[column].iloc[i] = mean_filler
        return well

        

class Calculator:

    #   FUNCTION calc_poissons_constant( y = Youngs modulus, S = Shears modulus )
    #
    #   description: this function will use the rela`tionship between Youngs modulus, Shears modulus, and Poissons constant
    #   v = Poissons constant = (y / 2 * s) - 1
    #
    def calc_poissons_constant(self, y, s):
        return (y / 2 * s) - 1

    #   FUNCTION flag_outliers( DataFrame )
    #   
    #   description: this function is used to calculate the outliers in our data sets based upon the iqr
    #
    def flag_outliers(self, data):
        outliers = []
        
        #   the function begins by taking the columns that have float values and iterating them one whole column at a time
        for col in data:
            #   this variable holds the column index 
            x = df.columns.get_loc(col)

            print(data[col].tolist())
            #   lower and upper are set to the threshold of where we would consider our data to be outlying
            lower, upper = self.outlier_treatment(data[col].tolist())
            
            # print(x, (upper, lower), data[col].tolist())
            for y in range(0, len(data[col])):
                if (data[col][y] > upper or data[col][y] < lower):
                    outliers.append((x, y))
        
        return outliers

    #   FUNCTION outlier_treatment( DataFrame_column ) 
    #
    #   description: this function calculates the outlying data within a given column of data from a DataFrame
    def outlier_treatment(self, data_col):
        #   sorts a data column to be in numerical order (least to greatest)
        data_col = sorted(data_col)
        #   creats q1 and q3 by running np.percentile( data_column, [lower_bound, upper_bound] )
        q1, q3 = np.percentile(data_col, [25, 75])
        #   uses q3 and q1 to calculate the interquartile range of the data column
        iqr = q3 - q1

        #   creates a lower and upper bound based upon the earlier calculated interquartile range
        lower_range = q1 - (1.5 * iqr)
        upper_range = q3 + (1.5 * iqr)

        return lower_range, upper_range


df = pd.read_csv('wellbore_data_producer_wells.csv')

well_ID_unique = df.Well_ID.unique()

def instantiate_wells(df):
    wells = []
    well = Well(df[df.Well_ID == 'Well_no_2'])
    wells.append(well)
    # for x in well_ID_unique:
    #     well = Well(df[df.Well_ID == x])
    #     wells.append(well)
    return wells

wells = instantiate_wells(df)

calc = Calculator()
data_floats = df.select_dtypes(include=[np.float64])
