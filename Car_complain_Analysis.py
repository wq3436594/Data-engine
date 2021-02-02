# -*- coding: utf-8 -*-
"""
Created on Tue Feb  2 09:03:52 2021

@author: wangbowen
"""

# Analyze the complain info. of vehicles

import pandas as pd

# load car_complain.csv document
result = pd.read_csv('car_complain.csv')
#print(result)

#Split the column 'problem' with all classifications
result = result.drop('problem', 1).join(result.problem.str.get_dummies(','))
#print(result.columns)

#Complain classifications from 8th column to 181 column
tags = result.columns[7:]

#Date cleaning
def date_clean(x):
    x = x.replace('一汽-大众', '一汽大众')
    return x
result['brand'] = result['brand'].apply(date_clean)


#Get total of different brands, and total of different problem respectively
Date_total_brand = result.groupby(['brand'])['id'].agg(['count'])
Date_total_problem = result.groupby(['brand'])[tags].agg(['sum'])

Date_total_problem = Date_total_brand.merge(Date_total_problem, left_index = True, right_index = True, how = 'left')

#Reset the index column with method reset_index(DateFrameGroupBy → DateFrame)
Date_total_problem.reset_index(inplace = True)


#Sort according to total complains of different brands respectively
Date_total_problem = Date_total_problem.sort_values('count', ascending = False)

print(Date_total_problem)

#Save document
Date_total_problem.to_csv('temp.csv', index = False)

#Sort with designated column 'problem'
query = ('A11', 'sum')
print(Date_total_problem.sort_values(query, ascending = False))



