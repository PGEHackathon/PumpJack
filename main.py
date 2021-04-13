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
calc = Calculator()
data_floats = df.select_dtypes(include=[np.float64])
rock = df['Rock facies']
y_col = data_floats['Youngs modulus, GPa']
s_col = data_floats['Shear modulus, GPa']

x = 1
y_Na = y_col.isna().sum()
s_Na = s_col.isna().sum()
#while x < 1460:
  #  print("Rock Facies:\t", rock[x], "\nYoungs modulus:\t", y_col[x], "\nShears modulus:\t", s_col[x], "\nPoissons constant:\t", calc.calc_poissons_constant(y_col[x], s_col[x]), "\n")
 #   x += 1

wells = df['Well_ID']
#   y = kg*m/(m^2*s^2) * s^3/m
y = df['Shear modulus, GPa'].isna().sum()

def facies_fill_in(df):
    i = len(df['X, m'])
    print(df['Rock facies'])
facies_fill_in(df)