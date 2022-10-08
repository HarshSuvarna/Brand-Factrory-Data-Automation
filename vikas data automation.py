import pandas as pd
import re
from IPython.display import display

v_data = pd.read_excel('BF Members W41.xlsx')

#print(v_data.columns)
##########################################Data Massaging###################################################################################

v_data.rename(columns = {'Store Code':'Store_Code','BTF Customer Mobile No.':'Mobile_no','Transaction No':'Transaction_No','Bill End Time':'Bill_End_Time'}, inplace = True)

v_data.drop(columns=['Count','Frequency'],inplace=True)

v_data['Freq'] = 1
####################################################Actual Code#################################################################################

def isValid(s):
    # 1) Begins with 0 or 91
    # 2) Then contains 7 or 8 or 9.
    # 3) Then contains 9 digits
    Pattern = re.compile("(0|91)?[7-9][0-9]{9}") #for pattern matching
    if Pattern.match(s):

        return 'Valid number'
    else:
        return 'Invalid number'


v_data['Mobile_no']=v_data['Mobile_no'].apply(str)
v_data['Remark'] = v_data['Mobile_no'].apply(isValid)

v_data._set_value(v_data.loc[v_data.duplicated(subset=['Mobile_no'],keep=False), :].index, 'Remark', 'Duplicate')

v_data.loc[v_data['Mobile_no'] == '--','Remark'] = 'Blank'

Number_counts = v_data.groupby('Mobile_no')[['Mobile_no','Freq']].sum()

Number_counts.reset_index(inplace=True)

v_data = pd.merge(v_data,Number_counts,how='left', on='Mobile_no')

#################################################Output Data Massaging#######################################################################################

v_data.drop(columns=['Freq_x'], inplace=True)
v_data.rename(columns={'Freq_y':'Frequency'}, inplace=True)

#v_data.to_excel("vikas_final_output.xlsx")

display(v_data[v_data['Mobile_no']=='49'])