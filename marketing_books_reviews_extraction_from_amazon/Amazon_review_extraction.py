'''
********************************************************
Created By:- Piyush Kumar
Date:- 11-DEC-2020
********************************************************
'''

# Importing required libraries
from selenium.webdriver import Chrome 
import time
from tqdm import tqdm
import random
import re
import pandas as pd

# Opening chrome browser
driver = Chrome('chromedriver.exe')
# OPening browser in full window
driver.maximize_window()

# List to store web page's links of marketing books
link = []
# List to store titles of marketing books
title = []

# opening the link in browser
driver.get('https://www.amazon.com/b?node=2702')
# iteration variable to extarct data from each book one by one in a webpage
i = 1
# loop until extracted the data of all books present in opned webpage
while(True):
    try:
        # pointing to a section where book title and link are present
        ele = driver.find_element_by_xpath('/html/body/div[2]/div[3]/div/div[1]/div/div[2]/div[2]/ul/li['+str(i)+']/div/div/div/div[2]/div[1]/div[1]/a')
        # Add extracted title in title list
        title.append(ele.text)
        # Add extracted link in link list
        link.append(ele.get_attribute('href'))
        # incrementing interation variable
        i+=1
    except:
        # When get an exception then it means data of all books in the webpage have been extracted hence break the loop
        break

# Performing pagination
# Loop until opened all webpages contaning marketing books.
for page_number in tqdm(range(2,76)):
    # opening the starting web page in the browser
    driver.get('https://www.amazon.com/s?rh=n%3A283155%2Cn%3A%211000%2Cn%3A3%2Cn%3A2698%2Cn%3A2702&page='+str(page_number))
    # increment variable to extarct data from each book one by one in a webpage
    i = 1
    # loop until extracted the data of all books present in opned webpage
    while(True):
        try:
            # random time delay
            time.sleep(random.uniform(0,3))
            # extracting book title
            ele_text = driver.find_element_by_xpath('/html/body/div[1]/div[1]/div[1]/div[2]/div/span[3]/div[2]/div['+str(i)+']/div/span/div/div/div[2]/div[2]/div/div[1]/div/div/div[1]/h2/a')
            title.append(ele_text.text)
            # extracting webpage link of the book
            ele_link = driver.find_element_by_xpath('/html/body/div[1]/div[1]/div[1]/div[2]/div/span[3]/div[2]/div['+str(i)+']/div/span/div/div/div[2]/div[2]/div/div[1]/div/div/div[1]/h2/a')
            link.append(ele_link.get_attribute('href'))
            i+=1
        except:
            # got an exception means all webpages have been visited and hence break the loop.
            break

# List to store publication date of books
publish_date = []
# List to store links where the reviews of books are present
review_link = []

# opening book web page link one by one 
for lnk in tqdm(link):
    # open the link in the browser
    driver.get(lnk)
    try:
        # random time delay
        time.sleep(random.uniform(0,2))
        # extracting publication date
        ele = driver.find_element_by_class_name('detail-bullet-list').text
        ele = re.findall('\nPublisher.*\n',ele)[0][1:-1]
        publish_date.append(re.findall('\(.*\)',ele)[0][1:-1])
    except:
        try:
            # extracting publication date for books whoose publication dates can't be extracted by first logic
            ele = driver.find_element_by_class_name('a-span6').text
            ele = re.findall('\Date.*\n',ele)[0]
            ele = ele.replace('Date','')[1:-1]
            publish_date.append(ele)
        except:
            publish_date.append(' ')
            
    try:
        # random time delay
        time.sleep(random.uniform(0,2))
        # extracting review webpage links
        link = driver.find_element_by_partial_link_text('all reviews')
        review_link.append(link.get_attribute('href'))
    except:
        review_link.append(' ')

# list to store total review count of each books under marketing category
review_count = []
# opening each review webpage one by one
for link in tqdm(review_link):
    try:
        driver.get(link)
        time.sleep(random.uniform(0,3))
        # extracting review count
        txt = driver.find_element_by_id('filter-info-section').text.split('|')[1]
        review_count.append(''.join(re.findall('[0-9]',txt)))
    except:
        review_count.append(' ')
        
# converting string values into integer values for review_count list
reviews = []
for count in review_count:
    try:
        reviews.append(int(count))
    except:
        reviews.append(0)

# creating dataframe to store book title, book publication date and review count
data = pd.DataFrame((title,publish_date,reviews,review_link)).T
data.columns = ['Title', 'Publication Date', 'Review Count', 'Review Link']

# Filtering those books which have more than 100 reviews
data = data[data['Review Count']>100]
data = data.reset_index(drop=True)

# Extracting one star, two star, three star, four star and five star reviews one by one for all books
links = data['Review Link']

star = ['&filterByStar=one_star&pageNumber=1',
        '&filterByStar=two_star&pageNumber=1',
        '&filterByStar=three_star&pageNumber=1',
        '&filterByStar=four_star&pageNumber=1',
        '&filterByStar=five_star&pageNumber=1']

print('Extracting one star reviews......')
one_star_reviews = []
for link in tqdm(links):
    reviews = []
    url = link+star[0]
    driver.get(url)
    while(True):
        ele = driver.find_elements_by_class_name('review-text-content')
        for i in ele:
            reviews.append(i.text)
        try:
            next_page_link = driver.find_element_by_css_selector('#cm_cr-pagination_bar > ul > li.a-last > a').get_attribute('href')
            time.sleep(random.uniform(1,3))
            driver.get(next_page_link)
        except:
            break
    one_star_reviews.append(reviews)

print('Extracting two star reviews.....')
two_star_reviews = []
for link in tqdm(links):
    reviews = []
    url = link+star[1]
    driver.get(url)
    while(True):
        ele = driver.find_elements_by_class_name('review-text-content')
        for i in ele:
            reviews.append(i.text)
        try:
            next_page_link = driver.find_element_by_css_selector('#cm_cr-pagination_bar > ul > li.a-last > a').get_attribute('href')
            time.sleep(random.uniform(1,3))
            driver.get(next_page_link)
        except:
            break
    two_star_reviews.append(reviews)

print('Extracting three star reviews....')
three_star_reviews = []
for link in tqdm(links):
    reviews = []
    url = link+star[2]
    driver.get(url)
    while(True):
        ele = driver.find_elements_by_class_name('review-text-content')
        for i in ele:
            reviews.append(i.text)
        try:
            next_page_link = driver.find_element_by_css_selector('#cm_cr-pagination_bar > ul > li.a-last > a').get_attribute('href')
            time.sleep(random.uniform(1,3))
            driver.get(next_page_link)
        except:
            break
    three_star_reviews.append(reviews)

print('Extrcating four star reviews....')
four_star_reviews = []
for link in tqdm(links):
    reviews = []
    url = link+star[3]
    driver.get(url)
    while(True):
        ele = driver.find_elements_by_class_name('review-text-content')
        for i in ele:
            reviews.append(i.text)
        try:
            next_page_link = driver.find_element_by_css_selector('#cm_cr-pagination_bar > ul > li.a-last > a').get_attribute('href')
            time.sleep(random.uniform(1,3))
            driver.get(next_page_link)
        except:
            break
    four_star_reviews.append(reviews)

print('Extrcating five star reviews....')
five_star_reviews = []
for link in tqdm(links):
    reviews = []
    url = link+star[4]
    driver.get(url)
    while(True):
        ele = driver.find_elements_by_class_name('review-text-content')
        for i in ele:
            reviews.append(i.text)
        try:
            next_page_link = driver.find_element_by_css_selector('#cm_cr-pagination_bar > ul > li.a-last > a').get_attribute('href')
            time.sleep(random.uniform(1,3))
            driver.get(next_page_link)
        except:
            break
    five_star_reviews.append(reviews)

# saving extracted data into an excel file.    
df1 = pd.DataFrame((five_star_reviews[0], four_star_reviews[0], three_star_reviews[0], two_star_reviews[0],one_star_reviews[0])).T
df1.columns = ['Five star review', 'Four star review', 'Three star review', 'Two star review', 'One star review']
df1.insert(0,'Book title',data.iloc[0][0])
df1.insert(1,'Publication date',data.iloc[0][1])
df1.insert(2,'Review count', data.iloc[0][2])

for i in tqdm(range(1,len(data))):
    df2 = pd.DataFrame((five_star_reviews[i], four_star_reviews[i], three_star_reviews[i], two_star_reviews[i],one_star_reviews[i])).T
    df2.columns = ['Five star review', 'Four star review', 'Three star review', 'Two star review', 'One star review']
    df2.insert(0,'Book title',data.iloc[i][0])
    df2.insert(1,'Publication date',data.iloc[i][1])
    df2.insert(2,'Review count', data.iloc[i][2])
    
    df1 = pd.concat((df1,df2),axis = 0, ignore_index=True)
    
df1.to_excel('Marketing_Books_Review_data.xlsx',index=False)