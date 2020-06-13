import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import datetime as dt
import ds_useful
import math

raw_data = pd.read_csv('Comcast_telecom_complaints_data.csv')
#print(raw_data.dtypes)
# getting the data in required form
raw_data['Ticket #'].replace('comcas', 000000, inplace=True)
raw_data['Ticket #'] = raw_data['Ticket #'].astype(int)
raw_data['DatenTime'] = raw_data['Date'] + ' ' + raw_data['Time']
raw_data['DatenTime'] = pd.to_datetime(raw_data['DatenTime'])
# Dropping few columns
raw_data.drop(['Date', 'Date_month_year', 'Time'], axis=1, inplace=True)
raw_data.columns = ['Incident','Complain','Received','city','State','Code','Status','Other_Filing','DatenTime']
#print(raw_data.dtypes)
# plotting Single Variables
'''
for i in ['Status', 'Other_Filing']:
    #table = raw_data[i].value_counts()
    #plt.pie(x=table, labels=table.index, shadow=True, autopct='%1.0f%%')
    sns.countplot(x=raw_data[i], palette="Set3")
    plt.show()
'''
# Cutting Section for plotting and viewing
view_data = pd.DataFrame(raw_data.loc[:, ['DatenTime', 'Incident']])
view_data.set_index(view_data.DatenTime, inplace=True)
view_data['year'] = view_data.index.year
view_data['month'] = view_data.index.month
view_data['day'] = view_data.index.day
view_data['date'] = view_data.index.date
#print(view_data)

for i in ['month', 'day','date']:
    plt.figure(figsize=(10, 10))
    temp = pd.DataFrame(view_data[i].value_counts())
    plt.subplot(1, 2, 1)
    sns.countplot(x=view_data[i])
    plt.subplot(1, 2, 2)
    sns.lineplot(y=temp[i], x=temp.index, data=view_data)
    plt.show()
sns.countplot(x=raw_data['Received'])
plt.show()


fre_table ={'Internet':0,'Network':0,'other':0}
for i in raw_data['Complain']:
    if 'Internet' in str(i):
        fre_table['Internet'] += 1
    if 'network' in str(i):
        fre_table['Network'] += 1
    else:
        fre_table['other'] += 1
print(fre_table)

ct = pd.crosstab(raw_data['State'], raw_data['Status'])
ct.plot.bar(stacked=True)
plt.legend(title='mark')
plt.show()
raw_data['State'].value_counts().plot.bar()
plt.title = 'Highest no of Counts'
plt.show()
print(ct)
ct['Unresolved'] = ct['Open'] + ct['Pending']
ct['Resolved_total'] = ct['Closed']+ct['Solved']
sum_unresol = sum(ct['Unresolved'])
sum_resol = sum(ct['Resolved_total'])
ct['Unresolved_Per'] = (ct['Unresolved']/sum_unresol)*100
print(ct.sort_values(by='Unresolved_Per', ascending=False))
print('The maximum Percentage of Unresolved Incidents are {} from {}'.format(15.47388, 'Georgia'))
print(ct.loc[ct['Unresolved_Per'].max() == ct['Unresolved_Per']])
#print(raw_data.loc[((raw_data['Status'] == 'Solved') or (raw_data['Status'] == 'Closed')) & (raw_data['Received'] == 'Internet'), ['Incident']])
res1 = raw_data.loc[(raw_data['Status'].isin(['Solved','Closed'])) & (raw_data['Received']=='Internet'),['Incident']]
res2 = raw_data.loc[(raw_data['Status'].isin(['Solved','Closed'])) & (raw_data['Received']=='Customer Care Call'),['Incident']]
print('The Percentage of Resolved which were received from Internet is {}'.format((res1.shape[0]/sum_resol)*100))
print('The Percentage of Resolved which were received from Customer Care Call is {}'.format((res2.shape[0]/sum_resol)*100))