# This script adds race_held_next_year data to pm1 columns

# Importing required modules

import pandas as pd

# Specifying the path to the data -- update this accordingly!

username = ''
filepath = 'C:/Users/' + username + '/Documents/Data/ultraCOVID/'

# Reading in the race data

ultradata = pd.read_csv(filepath + 'ultradata.csv')

# Updating race info columns as needed

c1 = ultradata['NY_Event_Name_PM1'].to_list()
c2 = ultradata['NY_Event_Distance_PM1'].to_list()
c3 = ultradata['NY_RACE_City'].to_list()
c4 = ultradata['NY_RACE_State'].to_list()

cc1 = ultradata['RACE_Name'].to_list()
cc2 = ultradata['RACE_Distance'].to_list()
cc3 = ultradata['RACE_City'].to_list()
cc4 = ultradata['RACE_State'].to_list()

c1 = [c1[i] if str(c1[i]) != 'nan' else cc1[i] for i in range(len(c1))]
c2 = [c2[i] if str(c2[i]) != 'nan' else cc2[i] for i in range(len(c2))]
c3 = [c3[i] if str(c3[i]) != 'nan' else cc3[i] for i in range(len(c3))]
c4 = [c4[i] if str(c4[i]) != 'nan' else cc4[i] for i in range(len(c4))]

# Updating covid data columns as needed

c5 = ultradata['Runner_City_Cases_MA7_PM1'].to_list()
c6 = ultradata['Runner_City_Cases_MA14_PM1'].to_list()
c7 = ultradata['Runner_City_Cases_MA30_PM1'].to_list()
c8 = ultradata['Runner_City_Deaths_MA7_PM1'].to_list()
c9 = ultradata['Runner_City_Deaths_MA14_PM1'].to_list()
c10 = ultradata['Runner_City_Deaths_MA30_PM1'].to_list()
c11 = ultradata['Runner_State_Cases_MA7_PM1'].to_list()
c12 = ultradata['Runner_State_Cases_MA14_PM1'].to_list()
c13 = ultradata['Runner_State_Cases_MA30_PM1'].to_list()
c14 = ultradata['Runner_State_Deaths_MA7_PM1'].to_list()
c15 = ultradata['Runner_State_Deaths_MA14_PM1'].to_list()
c16 = ultradata['Runner_State_Deaths_MA30_PM1'].to_list()
c17 = ultradata['Race_City_Cases_MA7_PM1'].to_list()
c18 = ultradata['Race_City_Cases_MA14_PM1'].to_list()
c19 = ultradata['Race_City_Cases_MA30_PM1'].to_list()
c20 = ultradata['Race_City_Deaths_MA7_PM1'].to_list()
c21 = ultradata['Race_City_Deaths_MA14_PM1'].to_list()
c22 = ultradata['Race_City_Deaths_MA30_PM1'].to_list()
c23 = ultradata['Race_State_Cases_MA7_PM1'].to_list()
c24 = ultradata['Race_State_Cases_MA14_PM1'].to_list()
c25 = ultradata['Race_State_Cases_MA30_PM1'].to_list()
c26 = ultradata['Race_State_Deaths_MA7_PM1'].to_list()
c27 = ultradata['Race_State_Deaths_MA14_PM1'].to_list()
c28 = ultradata['Race_State_Deaths_MA30_PM1'].to_list()

cc5 = ultradata['Runner_City_Cases_MA7'].to_list()
cc6 = ultradata['Runner_City_Cases_MA14'].to_list()
cc7 = ultradata['Runner_City_Cases_MA30'].to_list()
cc8 = ultradata['Runner_City_Deaths_MA7'].to_list()
cc9 = ultradata['Runner_City_Deaths_MA14'].to_list()
cc10 = ultradata['Runner_City_Deaths_MA30'].to_list()
cc11 = ultradata['Runner_State_Cases_MA7'].to_list()
cc12 = ultradata['Runner_State_Cases_MA14'].to_list()
cc13 = ultradata['Runner_State_Cases_MA30'].to_list()
cc14 = ultradata['Runner_State_Deaths_MA7'].to_list()
cc15 = ultradata['Runner_State_Deaths_MA14'].to_list()
cc16 = ultradata['Runner_State_Deaths_MA30'].to_list()
cc17 = ultradata['Race_City_Cases_MA7'].to_list()
cc18 = ultradata['Race_City_Cases_MA14'].to_list()
cc19 = ultradata['Race_City_Cases_MA30'].to_list()
cc20 = ultradata['Race_City_Deaths_MA7'].to_list()
cc21 = ultradata['Race_City_Deaths_MA14'].to_list()
cc22 = ultradata['Race_City_Deaths_MA30'].to_list()
cc23 = ultradata['Race_State_Cases_MA7'].to_list()
cc24 = ultradata['Race_State_Cases_MA14'].to_list()
cc25 = ultradata['Race_State_Cases_MA30'].to_list()
cc26 = ultradata['Race_State_Deaths_MA7'].to_list()
cc27 = ultradata['Race_State_Deaths_MA14'].to_list()
cc28 = ultradata['Race_State_Deaths_MA30'].to_list()

c5 = [c5[i] if str(c5[i]) != 'nan' else cc5[i] for i in range(len(c5))]
c6 = [c6[i] if str(c6[i]) != 'nan' else cc6[i] for i in range(len(c6))]
c7 = [c7[i] if str(c7[i]) != 'nan' else cc7[i] for i in range(len(c7))]
c8 = [c8[i] if str(c8[i]) != 'nan' else cc8[i] for i in range(len(c8))]
c9 = [c9[i] if str(c9[i]) != 'nan' else cc9[i] for i in range(len(c9))]
c10 = [c10[i] if str(c10[i]) != 'nan' else cc10[i] for i in range(len(c10))]
c11 = [c11[i] if str(c11[i]) != 'nan' else cc11[i] for i in range(len(c11))]
c12 = [c12[i] if str(c12[i]) != 'nan' else cc12[i] for i in range(len(c12))]
c13 = [c13[i] if str(c13[i]) != 'nan' else cc13[i] for i in range(len(c13))]
c14 = [c14[i] if str(c14[i]) != 'nan' else cc14[i] for i in range(len(c14))]
c15 = [c15[i] if str(c15[i]) != 'nan' else cc15[i] for i in range(len(c15))]
c16 = [c16[i] if str(c16[i]) != 'nan' else cc16[i] for i in range(len(c16))]
c17 = [c17[i] if str(c17[i]) != 'nan' else cc17[i] for i in range(len(c17))]
c18 = [c18[i] if str(c18[i]) != 'nan' else cc18[i] for i in range(len(c18))]
c19 = [c19[i] if str(c19[i]) != 'nan' else cc19[i] for i in range(len(c19))]
c20 = [c20[i] if str(c20[i]) != 'nan' else cc20[i] for i in range(len(c20))]
c21 = [c21[i] if str(c21[i]) != 'nan' else cc21[i] for i in range(len(c21))]
c22 = [c22[i] if str(c22[i]) != 'nan' else cc22[i] for i in range(len(c22))]
c23 = [c23[i] if str(c23[i]) != 'nan' else cc23[i] for i in range(len(c23))]
c24 = [c24[i] if str(c24[i]) != 'nan' else cc24[i] for i in range(len(c24))]
c25 = [c25[i] if str(c25[i]) != 'nan' else cc25[i] for i in range(len(c25))]
c26 = [c26[i] if str(c26[i]) != 'nan' else cc26[i] for i in range(len(c26))]
c27 = [c27[i] if str(c27[i]) != 'nan' else cc27[i] for i in range(len(c27))]
c28 = [c28[i] if str(c28[i]) != 'nan' else cc28[i] for i in range(len(c28))]

# Replacing these columns in the data frame

drip_drip_DROP = ['NY_Event_Name_PM1', 'NY_Event_Distance_PM1', 'NY_RACE_City',
                  'NY_RACE_State', 'Runner_City_Cases_MA7_PM1', 'Runner_City_Cases_MA14_PM1',
                  'Runner_City_Cases_MA30_PM1', 'Runner_City_Deaths_MA7_PM1',
                  'Runner_City_Deaths_MA14_PM1', 'Runner_City_Deaths_MA30_PM1',
                  'Runner_State_Cases_MA7_PM1', 'Runner_State_Cases_MA14_PM1',
                  'Runner_State_Cases_MA30_PM1', 'Runner_State_Deaths_MA7_PM1',
                  'Runner_State_Deaths_MA14_PM1', 'Runner_State_Deaths_MA30_PM1',
                  'Race_City_Cases_MA7_PM1', 'Race_City_Cases_MA14_PM1',
                  'Race_City_Cases_MA30_PM1', 'Race_City_Deaths_MA7_PM1',
                  'Race_City_Deaths_MA14_PM1', 'Race_City_Deaths_MA30_PM1',
                  'Race_State_Cases_MA7_PM1', 'Race_State_Cases_MA14_PM1',
                  'Race_State_Cases_MA30_PM1', 'Race_State_Deaths_MA7_PM1',
                  'Race_State_Deaths_MA14_PM1', 'Race_State_Deaths_MA30_PM1']

ultradata = ultradata.drop(drip_drip_DROP, axis = 1)

c1 = pd.Series(c1, name = drip_drip_DROP[0])
c2 = pd.Series(c2, name = drip_drip_DROP[1])
c3 = pd.Series(c3, name = drip_drip_DROP[2])
c4 = pd.Series(c4, name = drip_drip_DROP[3])
c5 = pd.Series(c5, name = drip_drip_DROP[4])
c6 = pd.Series(c6, name = drip_drip_DROP[5])
c7 = pd.Series(c7, name = drip_drip_DROP[6])
c8 = pd.Series(c8, name = drip_drip_DROP[7])
c9 = pd.Series(c9, name = drip_drip_DROP[8])
c10 = pd.Series(c10, name = drip_drip_DROP[9])
c11 = pd.Series(c11, name = drip_drip_DROP[10])
c12 = pd.Series(c12, name = drip_drip_DROP[11])
c13 = pd.Series(c13, name = drip_drip_DROP[12])
c14 = pd.Series(c14, name = drip_drip_DROP[13])
c15 = pd.Series(c15, name = drip_drip_DROP[14])
c16 = pd.Series(c16, name = drip_drip_DROP[15])
c17 = pd.Series(c17, name = drip_drip_DROP[16])
c18 = pd.Series(c18, name = drip_drip_DROP[17])
c19 = pd.Series(c19, name = drip_drip_DROP[18])
c20 = pd.Series(c20, name = drip_drip_DROP[19])
c21 = pd.Series(c21, name = drip_drip_DROP[20])
c22 = pd.Series(c22, name = drip_drip_DROP[21])
c23 = pd.Series(c23, name = drip_drip_DROP[22])
c24 = pd.Series(c24, name = drip_drip_DROP[23])
c25 = pd.Series(c25, name = drip_drip_DROP[24])
c26 = pd.Series(c26, name = drip_drip_DROP[25])
c27 = pd.Series(c27, name = drip_drip_DROP[26])
c28 = pd.Series(c28, name = drip_drip_DROP[27])

soootired = [ultradata, c1, c2, c3, c4, c5, c6, c7, c8, c9, c10, c11, c12, c13, c14,
             c15, c16, c17, c18, c19, c20, c21, c22, c23, c24, c25, c26, c27, c28]

ultradata = pd.concat(soootired, axis = 1)

# Writing the final data frame to file

ultradata.to_csv(filepath + 'ultradata.csv', index = False)

