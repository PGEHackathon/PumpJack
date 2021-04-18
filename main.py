import numpy as np
import pandas as pd
import math

df = pd.read_csv('wellbore_data_producer_wells.csv')
well_ID_unique = df.Well_ID.unique()

class Well:
    #
    #   FUNCTION __init()__
    #
    #   description: takes the individual column value for the row being evaluated and puts this data into the Well object
    # 

    def __init__(self, well):
        #   id = well_no
        self.id = well['Well_ID'].unique()[0]
        self.well_number = int(self.id[-1])
        #   x = unique x value (meters) in the 20 pieces of data
        self.x = well['X, m'].unique()[0]
        #   y = unique y value (meters) in the 20 pieces of data
        self.y = well['Y, m'].unique()[0]

        # self.attributes = []
        print(well)
        well = self.threshold_nan_filler(well, self.well_number * 20)
        print(well)
        # for x in well.columns:
        #     self.attributes.append((x, list(well.loc[:, x].values)))
        
    def threshold_nan_filler(self, well, i):
        # create for loop to run through each column and return percent NaN 
        j = 0
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
                print(j)
                while j < i:
                    print(well.iloc[j, np.where(well_ID_unique == column)], "\t is nan:", math.isnan(well.at[j, column]))
                    if math.isnan(well.at[j, column]):
                        well.iloc[j, np.where(well_ID_unique == column)] = mean_filler
        return well

def instantiate_wells(df):
    wells = []
    well = Well(df[df.Well_ID == 'Well_no_2'])
    wells.append(well)
    # for x in well_ID_unique:
    #     well = Well(df[df.Well_ID == x])
    #     wells.append(well)
    return wells

wells = instantiate_wells(df)

#y_prod = pd.read_csv('production_history')
#y_prod = y_prod.drop(columns=['Cumulative Water production (1 yr), MSTB', 'Cumulative Water production (2 yr), MSTB', 'Cumulative Water production (3 yr), MSTB'])