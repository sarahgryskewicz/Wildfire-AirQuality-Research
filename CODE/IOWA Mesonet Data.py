import pandas as pd
import numpy as np
import matplotlib as mplt
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from windrose import WindroseAxes
from matplotlib import rcParams
from matplotlib import rc
rc('mathtext', default='regular') 
rcParams['font.family'] = 'Tahoma'
rcParams['mathtext.fontset'] = 'cm'
rcParams['mathtext.rm'] = 'Tahoma'

####################
# First make time series plots
####################
# Read in data
filelist = '/Users/Desktop/REU/Weather Activity/IOWA (ASOS Data)/'
gfiles=sorted(glob.glob(filelist+'*txt'))

# Initialize an empty list to hold individual DataFrames
dfs = []

# Read each text file into a DataFrame and append to the list
for file in gfiles:
    df = pd.read_csv(file)  # Adjust separator if needed
    dfs.append(df)

# Concatenate all DataFrames in the list along rows (axis=0)
df = pd.concat(dfs, ignore_index=True)
sitenames=df['station'].unique()


# Group by 'Date' and calculate regional average
df_regional_avg = df.groupby('day')['avg_rh'].mean().reset_index()
df_regional_avg


### Make a plot of avg temp vs avg_feel w/ the below code
df['avg_temp']=None
avg_temp=[]
for i in range(0, len(df['max_temp_f'])):
    a = ((df['max_temp_f'][i] + df['min_temp_f'][i])//2)
    avg_temp.append(a)

df['avg_temp']=avg_temp
df_regional_avgT = df.groupby('day')['avg_temp'].mean().reset_index()
df_regional_avgT

df_regional_avgF = df.groupby('day')['avg_feel'].mean().reset_index()
df_regional_avgF


diff = []
for i in range(0, len(df_regional_avgT['avg_temp'])):
    difference = df_regional_avgF['avg_feel'][i] - df_regional_avgT['avg_temp'][i]
    difference = round(difference, 2)
    diff.append(difference)

# Make the plot
fig = plt.figure(figsize = (20,5))
fig.set_facecolor('whitesmoke')
plt.xticks(rotation=45, fontsize=10)
plt.xlabel('Date', fontsize=18)
plt.ylabel('Average Temp (F)', fontsize = 18)
plt.title('NE ASOS Temp (F) vs Avg Feel (F) June-July 2023', fontsize=20)
plt.plot(df_regional_avg['day'], df_regional_avgT['avg_temp'], label = 'NE regional avg temp', marker='o', color='r', alpha=0.5)
plt.legend(loc='upper left', fontsize=13)
plt.ylim(50,85)


ax = plt.twinx()
ax.set_facecolor('snow')
ax.plot(df_regional_avg['day'], df_regional_avgF['avg_feel'], label = 'NE regional avg feel', linestyle = '--', color='b', alpha=0.5)
ax.set_ylabel('Average Feel (F)', fontsize=18)
ax.set_ylim(50,85)
ax.legend(loc='upper right', fontsize=13)

## Highlight events of interest on the plot
# June 5: Start of first event
# June 9: End of first event
s_1 = '2023-06-05'
e_1 = '2023-06-08'
s1 = df_regional_avg.index[df_regional_avg['day'] == s_1][0]
e1 = df_regional_avg.index[df_regional_avg['day'] == e_1][0]

# June 15: Start of second event
# June 18: End of second event
s_2 = '2023-06-15'
e_2 = '2023-06-18'
s2 = df_regional_avg.index[df_regional_avg['day'] == s_2][0]
e2 = df_regional_avg.index[df_regional_avg['day'] == e_2][0]

# July 16: Start of third event
# July 18: End of third event
s_3 = '2023-07-16'
e_3 = '2023-07-18'
s3 = df_regional_avg.index[df_regional_avg['day'] == s_3][0]
e3 = df_regional_avg.index[df_regional_avg['day'] == e_3][0]

plt.axvspan(s1, e1, facecolor='seagreen', alpha=0.2)
plt.axvspan(s2, e2, facecolor = 'seagreen', alpha=0.2)
plt.axvspan(s3, e3, facecolor = 'seagreen', alpha=0.2)

"""
# zoom in on certain days below
s = '2023-07-15'
e = '2023-07-20'
start = df_regional_avg.index[df_regional_avg['day'] == s][0]
end = df_regional_avg.index[df_regional_avg['day'] == e][0]

plt.legend(loc='upper right',fontsize=12)
plt.xlim(start,end)

ax.set_ylim(65,85)
plt.ylim(65,85)
"""


fig = plt.figure(figsize = (20,5))
fig.set_facecolor('whitesmoke')

plt.xticks(rotation=45, fontsize=12)
plt.xlabel('Date', fontsize=18)
plt.ylabel('RH (%)', fontsize = 18)
plt.title('NE ASOS RH (%) vs Temp (F) June-July 2023', fontsize=20)
plt.plot(df_regional_avg['day'], df_regional_avg['avg_rh'], label = 'NE regional avg RH', marker='<', linestyle = '--', color='b', alpha=0.5)
plt.ylim(50,90)
plt.legend(loc='upper left', fontsize=13)

ax = plt.twinx()
ax.set_facecolor('snow')
ax.set_ylabel('Average Temp (F)', fontsize = 18)
ax.plot(df_regional_avg['day'], df_regional_avgT['avg_temp'], label = 'NE regional avg temp', marker='o', color='r', alpha=0.5)
ax.legend(loc='upper right', fontsize=13)
ax.set_ylim(50,90)

## Highlight events of interest on the plot
# June 5: Start of first event
# June 9: End of first event
s_1 = '2023-06-05'
e_1 = '2023-06-08'
s1 = df_regional_avg.index[df_regional_avg['day'] == s_1][0]
e1 = df_regional_avg.index[df_regional_avg['day'] == e_1][0]

# June 15: Start of second event
# June 18: End of second event
s_2 = '2023-06-15'
e_2 = '2023-06-19'
s2 = df_regional_avg.index[df_regional_avg['day'] == s_2][0]
e2 = df_regional_avg.index[df_regional_avg['day'] == e_2][0]

# July 16: Start of third event
# July 18: End of third event
s_3 = '2023-07-16'
e_3 = '2023-07-18'
s3 = df_regional_avg.index[df_regional_avg['day'] == s_3][0]
e3 = df_regional_avg.index[df_regional_avg['day'] == e_3][0]

plt.axvspan(s1, e1, facecolor='seagreen', alpha=0.2)
plt.axvspan(s2, e2, facecolor = 'seagreen', alpha=0.2)
plt.axvspan(s3, e3, facecolor = 'seagreen', alpha=0.2)

"""
# zoom in on certain days below
s = '2023-06-04'
e = '2023-06-09'
start = df_regional_avg.index[df_regional_avg['day'] == s][0]
end = df_regional_avg.index[df_regional_avg['day'] == e][0]

plt.legend(loc='upper right',fontsize=12)
plt.xlim(start,end)
#ax.set_ylim(50,70)
"""

#################### 
# Next: Make windrose plots
####################
df_regional_avgD = df.groupby('day')['avg_wind_drct'].mean().reset_index()
df_regional_avgW = df.groupby('day')['avg_wind_speed_kts'].mean().reset_index()

fig = plt.figure(figsize=(14, 8))
fig.set_facecolor('whitesmoke')

ax = WindroseAxes.from_ax()
ax.set_radii_angle(label=False)  # Remove radii labels

ax.bar(df_regional_avgD['avg_wind_drct'],df_regional_avgW['avg_wind_speed_kts'], normed=True, bins=np.arange(2,7,0.5))
ax.tick_params(axis='both', which='minor', labelsize=20)

# set the cardinal directions
for t in ax.get_xticklabels():
    plt.setp(t, fontsize=18, color="k", fontweight="bold")
    
ax.set_yticklabels([])  # Remove y-axis tick labels

ax.legend(title = 'Wind Speed (kts)', bbox_to_anchor=(1.05, 1), loc='upper left',borderaxespad=0,title_fontsize=20,fontsize=20)
ax.set_title('NE ASOS Wind Speed (kts) and Direction ($^{o}$) June-July 2023', fontsize=20)
plt.show()


# Plot wind rose for a specific time period
fig = plt.figure(figsize=(14, 8))
fig.set_facecolor('whitesmoke')
ax = WindroseAxes.from_ax()
ax.set_radii_angle(label=False)  # Remove radii labels

# zoom in on certain days below
s = '2023-07-10'
e = '2023-07-19'
start = df_regional_avgD.index[df_regional_avg['day'] == s][0]
end = df_regional_avgD.index[df_regional_avg['day'] == e][0]


filtered_avgD = df_regional_avgD.loc[start:end]
filtered_avgW = df_regional_avgW.loc[start:end]

ax.bar(filtered_avgD['avg_wind_drct'], filtered_avgW['avg_wind_speed_kts'], normed=True, bins=np.arange(2, 5.5, 0.5))

ax.tick_params(axis='both', which='minor', labelsize=20)

# set the cardinal directions
for t in ax.get_xticklabels():
    plt.setp(t, fontsize=18, color="k", fontweight="bold")

ax.set_yticklabels([])  # Remove y-axis tick labels


ax.legend(title = 'Wind Speed (kts)', bbox_to_anchor=(1.05, 1), loc='upper left',borderaxespad=0,title_fontsize=20,fontsize=20)
ax.set_title('10-19 July ASOS Wind Speed (kts) and Direction ($^{o}$)', fontsize=20)
plt.show()
