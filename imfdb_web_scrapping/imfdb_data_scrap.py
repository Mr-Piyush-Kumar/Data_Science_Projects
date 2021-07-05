# -*- coding: utf-8 -*-
"""
Created on Sun Nov 15 20:13:05 2020

@author: Piyush Kumar
"""

############# Importing required libraries #################
import pandas as pd                 # for data manuplation
import requests                     # for downloading the web-pages
from bs4 import BeautifulSoup       # for extracting required data from web-pages
import os                           # for performing operating system related operations like delete and create files
from tqdm import tqdm               # for showing the progress bar to track processing time
import time                         # for time delay
############################################################

############ Function to extracting links for each and every movies and tv shows ###########################
def get_all_links(url):
    # list to store all the extracted links
    movie_links = []
    # counter variable to track the page number
    page_number = 1
    # loop until no next page available 
    while(True):
        # variable to store the downloaded webpage of current url
        webpage = requests.get(url)
        # if downloading of webpage is unsuccessful then raise an exception
        if(webpage.status_code != 200):
            print('Not able to load the website!!!')
            raise Exception
        # now storing the downloaded webpage in a file
        open('sample.txt','wb').write(webpage.content)
        # list to store the downloaded webpage line by line
        html_data = []
        # now opening the file which contains the downloaded webpage
        with open('sample.txt','rb') as f:
            # reading the whole file
            lines = f.readlines()
            # iteration variable to iterate over each line in the webpage file
            i = 0
            # loop until processed each line in the file
            while(i < len(lines)):
                # coverting line from byte format to string format
                line = str(lines[i])
                # if line contains the infromation about firearm and starts with '<h2> Pages in category'
                if('<h2>Pages in category' in line):
                    # loop until got this line '<div class="printfooter">'
                    while(True):
                        # coverting line from byte format to string format
                        line = str(lines[i])
                        # if the line is '<div class="printfooter">' then break the loop
                        if('<div class="printfooter">' in line):
                            break
                        # appending line in the list 'html_data'
                        html_data.append(lines[i])
                        i+=1
                i+=1
        # deleting the file after processing it 
        os.remove('sample.txt')
        # create a new html file which will contain the data from list 'html_data'
        with open('sample.html','wb') as f:
            f.writelines(html_data)
        # open the created html file for reading it
        content = open('sample.html')
        # parsing the html file using beautiful soup library
        sp = BeautifulSoup(content,'html5lib')
        # closing the opened html file
        content.close()
        # deleting the html file after processing it
        os.remove('sample.html')
        # exracting all the links in html data
        a = sp.find_all('a',href=True)
        # create a dictionary to store links as value and link text as key
        links = dict()
        # iterating over all the extracted links
        for link in a:
            # adding each links one by one in the dictionary
            links[link.text] = link['href']
        
        # iterating over each key in the dictionary
        for key in links:
            # if key is not 'next 200' and 'previous 200' then store the value for that key in the list 'movie_links'
            if(key != 'next 200' and key!= 'previous 200'):
                movie_links.append(links[key])
        # if there is next page available then replace the current url with next page url othewise break the loop
        if('next 200' in links):
            url = links['next 200']
            print('Page number =',page_number)
            page_number+=1
            url = 'http://www.imfdb.org'+url
            print(url)
        else:
            break
    # return the list 'movie_links'
    return movie_links
######################################################################################################################

########### Function to extract the data from webpages of each link ##################################################
########### function argument:- a list of links ###############################################################################
def get_all_data(links_list):
    # creating a dataframe to store the extracted data in proper format
    movie_data = pd.DataFrame(columns=['Name','Firearm','Use count'])
    # iterating over each link in the list
    for url in tqdm(links_list):
        # adding 'http://www.imfdb.org' in each link 
        url = 'http://www.imfdb.org'+url
        # download the webpage for current url
        webpage = requests.get(url)
        # if downloading of webpage is unsuccessful then raise an exception 
        if(webpage.status_code != 200):
            print('Not able to load the website!!!')
            raise Exception
        # parsing the html webpage using beautiful soup library
        soup = BeautifulSoup(webpage.content, 'html5lib')
        # extracting all <h2> heddings
        ele = soup.find_all('h2')
        # extracting firearms names from all <h2> hedding's text and storing in a list
        firearms = [(i).text for i in ele[1:]]
        # creating a file to store the webpage
        open('sample.txt','wb').write(webpage.content)
        # list to store the use count of each firearm in the movie or tv show
        use_count = []
        # open the created file for reading it line by line
        with open('sample.txt','rb') as f:
            # reading the whole file 
            lines = f.readlines()
            # iteration variable to iterate over each line in the file
            i = 0
            # counter variable to count the use_count of a firearm in a movie
            count = 0
            # loop until last line in the file
            while(i<len(lines)):
                # coverting line from byte format to string format 
                line = str(lines[i])
                # if line starts with <h2> tag
                if(line.startswith("b'<h2>")):
                    count = 0
                    # loop until got another line starts with <h2> tag
                    while(i<len(lines)):
                        i+=1
                        try:
                            # coverting line from byte format to string format
                            line = str(lines[i])
                        except:
                            pass
                        # if line starts with '<div class="thumb tnone"' then increment the counter variable if below conditions passed
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
        # concatinating the dataframe for current movie url into globle dataframe
        movie_data = pd.concat((movie_data,data),axis=0)
    # returning the gloable dataframe which contains the data about firearms used in all movies/tv shows in IMFDB
    return movie_data

#############################################################################################################################################
print('********************MOVIES************************')
# calling function get_all_links() to get the links of all movies in IMFDB
movie_links = get_all_links('http://www.imfdb.org/wiki/Category:Movie')
###
print('Total movies =',len(movie_links))
# calling function get_all_data() to get the firearm data from each movie in IMFDB
print('Extracting firearms data from all movies................')
time.sleep(2)
movie_data = get_all_data(movie_links)
# storing the extracted data in a csv file
movie_data.to_csv('movie_data.csv',index = False)

#############################################################################################################################################
print('********************TV SHOWS************************')
# calling function get_all_links() to get the links of all tv shows in IMFDB
television_show_links = get_all_links('http://www.imfdb.org/wiki/Category:Television')
print('Total tv shows =',len(television_show_links))
###
# calling function get_all_data() to get the firearm data from each tv show in IMFDB
print('Extracting firearms data from all tv shows................')
time.sleep(2)
tv_show_data = get_all_data(television_show_links)
# storing the extracted data in a csv file
tv_show_data.to_csv('tv_show_data.csv', index = False)
############################################################################################################################################