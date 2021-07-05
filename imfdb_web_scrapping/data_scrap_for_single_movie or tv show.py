# -*- coding: utf-8 -*-
"""
Created on Sun Nov 15 23:02:55 2020

@author: Piyush Kumar
"""
############# Importing required libraries #################
import pandas as pd                   # for data manuplation
import requests                       # for downloading the web-pages
from bs4 import BeautifulSoup         # for extracting required data from web-pages
import os                             # for performing operating system related operations like delete and create files
import matplotlib.pyplot as plt       # for plotting graphs and charts
import seaborn as sns                 # for plotting graphs and charts
############################################################

# url for movie or tv show from which you want to extract firearm data
url = "http://www.imfdb.org/wiki/Flash,_The_-_Season_4"
# downloading the webpage from the url
webpage = requests.get(url)
# if downloading of webpage is unsuccessful then raise an exception
if(webpage.status_code != 200):
    print('Not able to load the website!!!')
    raise Exception
# parsing the html webpage using beautiful soup library to extract the required data
soup = BeautifulSoup(webpage.content, 'html5lib')
# finding all <h2> tags in the html webpage
ele = soup.find_all('h2')
# extracting firearm names from all <h2> tags and store in a list
firearms = [(i).text for i in ele[1:]]

# creating a file which will store the downloaded html file
open('sample.txt','wb').write(webpage.content)
# list to store the use count of each firearm used in a movie/tv show
use_count = []
# opening the created file for reading line by line
with open('sample.txt','rb') as f:
    # reading the whole file and store each line in the list 'lines'
    lines = f.readlines()
    # iteration variable to iterate over each line in the file
    i = 0
    # counter variable to count the use count of a firearm
    count = 0
    # loop until process the each line in the file
    while(i<len(lines)):
        # converting line into string format from byte format
        line = str(lines[i])
        # if line starts with <h2> tag then make the counter variable equal to zero 
        if(line.startswith("b'<h2>")):
            count = 0
            # loop until got another line which starts with <h2> tag
            while(i<len(lines)):
                i+=1
                try:
                    # converting line into string format from byte format
                    line = str(lines[i])
                except:
                    pass
                # if line starts with "b'<div class="thumb tnone"" then increment the counter variable if conditions satisfies
                if(line.startswith("b'<div class=\"thumb tnone\"")):
                    try:
                        # index no. where 'width=' is there in the line
                        index = line.find('width=')
                        # extracting width value
                        width = int(line[index+7:index+10])
                        # index no. where 'height=' is there in the line
                        index = line.find('height=')
                        # extracting height value
                        height = int(line[index+8:index+11])
                        # if height and width satisfies the following conditions
                        if(width >= 450 and height >= 200):
                            count+=1
                    except:
                        pass
                # if line starts with <h2> tag then break the loop
                if(line.startswith("b'<h2>")):
                    i-=1
                    # append the value of counter varaible into list 'use_count'
                    use_count.append(count)
                    break
        i+=1
    # append the value of counter varaible into list 'use_count'
    use_count.append(count)
# deleting the created file after processing it
os.remove('sample.txt')
# extracting the name of the movie from the webpage
movie_name = soup.find(attrs = {'id':'firstHeading'}).text.replace('\n','')
# list to store the movie name for each firearm used in a movie
movie = [movie_name]*len(use_count)
 # creating a dataframe to store the data extracted from current movie url
data = pd.DataFrame([movie,firearms,use_count]).T
# giving column names for the dataframe
data.columns = ['Name','Firearm','Use count']
# sorting the rows of dataframe according to the values of 'Use count' column in descending order
data = data.sort_values(by='Use count',ascending=False)
# taking only top 10 rows for visualization
data = data[0:10].reset_index()
# defining a figure for plotting bar chart
plt.figure(figsize=(8,5))
# creating the bar chart
ax = sns.barplot(data = data, y='Firearm', x = 'Use count')
# y value for annotation each bar in the bar chart
y_count=0.1
# annotating each bar in the bar chart
for p in ax.patches:
    ax.annotate(str(int(p.get_width())), (p.get_width()+0.05,y_count),color='blue')
    y_count+=1
# setting the title of the chart
plt.title('Firearms used in '+data['Name'][0],color='blue')
# setting xlable in the chart
plt.xlabel('Use Count',fontsize = 12,color='blue')
# setting ylable in the chart
plt.ylabel('Firearm Name',fontsize = 12,color = 'blue')
# setting x values range in the chart
plt.xticks(range(min(data['Use count']), max(data['Use count'])+2))
# finally dispalying the chart
plt.show()

