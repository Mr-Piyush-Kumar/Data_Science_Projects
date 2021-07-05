# -*- coding: utf-8 -*-
"""
Created on Sun Nov 15 23:11:55 2020

@author: Piyush Kumar
"""
############# Importing required libraries #################
import pandas as pd                    # for data manuplation
import matplotlib.pyplot as plt        # for plotting graphs and charts
import seaborn as sns                  # for plotting graphs and charts
############################################################

try:
    # loading movie_data.csv file for visualization
    movie_data = pd.read_csv('movie_data.csv')
    # loading tv_show_data.csv file for visualization
    tv_show_data = pd.read_csv('tv_show_data.csv')
except:
    # if the files are not present in the current directory then raise an exception
    raise Exception('Please download the data first by executing imfdb_data_scrap.py')

################ Creating bar chart for firearms used in movies only #################
# grouping the movie data according to firearms and sum the use count of each firearm from all movies
df_movie = movie_data.groupby('Firearm')['Use count'].sum()
# resetting the dataframe index
df_movie = df_movie.reset_index()
# sorting the dataframe according to use count values in descending order and then reset the index
df_movie = df_movie.sort_values(by='Use count', ascending=False).reset_index(drop=True)
# defining figure to plot the bar chart
plt.figure(figsize=(12,6))
# creating bar chart for top 10 used firearms
ax = sns.barplot(data=df_movie[0:10], x='Use count',y='Firearm')
# variable to annotate each bar in the bar chart
y_count=0.1
# annotating each bar one by one in the bar chart
for p in ax.patches:
    ax.annotate(str(int(p.get_width())), (p.get_width()+0.05,y_count),color='blue')
    y_count+=1
# setting title for the bar chart
plt.title('Most Used Firearms in Movies',color='blue')
# setting xlable for the bar chart
plt.xlabel('Use count',fontsize=12,color='blue')
# setting ylable for the bar chart
plt.ylabel('Firearm name',fontsize=12,color='blue')
# displaying the bar chart
plt.show()
##########################################################################################

################ Creating bar chart for firearms used in tv shows only #################
# grouping the movie data according to firearms and sum the use count of each firearm from all tv shows 
df_tv = tv_show_data.groupby('Firearm')['Use count'].sum()
# resetting the dataframe index
df_tv = df_tv.reset_index()
# sorting the dataframe according to use count values in descending order and then reset the index
df_tv = df_tv.sort_values(by='Use count', ascending=False).reset_index(drop=True)
# defining figure to plot the bar chart
plt.figure(figsize=(12,6))
# creating the bar chart
ax = sns.barplot(data=df_tv[0:10], x='Use count',y='Firearm')
# variable to annotate each bar in the bar chart
y_count=0.1
# annotating each bar one by one in the bar chart
for p in ax.patches:
    ax.annotate(str(int(p.get_width())), (p.get_width()+0.05,y_count),color='blue')
    y_count+=1
# setting title for the bar chart
plt.title('Most Used Firearms in TV Shows',color='blue')
# setting xlable for the bar chart
plt.xlabel('Use count',fontsize=12,color='blue')
# setting ylable for the bar chart
plt.ylabel('Firearm name',fontsize=12,color='blue')
# displaying the bar chart
plt.show()
##########################################################################################

################ Creating bar chart for firearms used in movies and tv shows combined #################
# concatinating the dataframes of both movies and tv shows
data = pd.concat((movie_data,tv_show_data),axis = 0)
# grouping the data according to the firearms and then sum the use count of each firearm used
df = data.groupby('Firearm')['Use count'].sum()
# resetting the index
df = df.reset_index()
# sorting the dataframe according to use count values in descending order and then reset the index
df = df.sort_values(by='Use count', ascending=False).reset_index(drop=True)
# defining the figure to plot the bar chart
plt.figure(figsize=(12,6))
# creating the bar chart
ax = sns.barplot(data=df[0:10], x='Use count',y='Firearm')
# variable to annotate each bar in the bar chart
y_count=0.1
# annotating each bar one by one in the bar chart
for p in ax.patches:
    ax.annotate(str(int(p.get_width())), (p.get_width()+0.05,y_count),color='blue')
    y_count+=1
# setting title for the bar chart
plt.title('Most Used Firearms in Movies and TV Shows combined',color='blue')
# setting xlable for the bar chart
plt.xlabel('Use count',fontsize=12,color='blue')
# setting ylable for the bar chart
plt.ylabel('Firearm name',fontsize=12,color='blue')
# displaying the bar chart
plt.show()
##########################################################################################

