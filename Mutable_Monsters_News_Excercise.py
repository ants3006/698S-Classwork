#!/usr/bin/env python
# coding: utf-8

# # News Scraping: APNews Health
# ##### Antonella Sciortino & Amil Arthur  

# In[24]:


#Import Libraries 
import requests
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import csv


# ### Obtain list of news from the coverpage

# In[25]:


# url definition
url = "https://apnews.com/apf-Health"


# In[26]:


#Retrive List of news

# Request
r1 = requests.get(url)


# We'll save in coverpage the cover page content
coverpage = r1.content

# Soup creation
soup = BeautifulSoup(coverpage)

# News identification
coverpage_news = soup.find_all(class_='FeedCard Component-wireStory-0-2-94 card-0-2-95')
len(coverpage_news)


# Now we have a list in which every element is a news article:

# In[19]:


coverpage_news[5]


# ### Let's extract the text from the articles

# In[20]:


# First, we'll define the number of articles we want
number_of_articles = 5


# In[21]:


# Lists for content, links and titles
news_contents = []
list_links = []
list_titles = []
list_dates = []

for n in np.arange(0, number_of_articles):
        

    
    # Getting the link of the article
    link = 'https://apnews.com' + coverpage_news[n].find('a')['href']
    list_links.append(link)
    
    # Getting the title
    title = coverpage_news[n].find('a').get_text()
    list_titles.append(title)
    
    #Get Article Date 
    dates = coverpage_news[n].find('span', class_= 'Timestamp Component-root-0-2-111 Component-timestamp-0-2-110').get_text()
    list_dates.append(dates)
    
    # Reading the content (it is divided in paragraphs)
    article = requests.get(link)
    article_content = article.content
    soup_article = BeautifulSoup(article_content)
    body = soup_article.find_all('div', class_='Article')
    x = body[0].find_all('p')
    
    # Unifying the paragraphs
    list_paragraphs = []
    for p in np.arange(0, len(x)):
        paragraph = x[p].get_text()
        list_paragraphs.append(paragraph)
        final_article = " ".join(list_paragraphs)
        
    news_contents.append(final_article)


# Save our news data from AP for later use into:
# * a dataframe object 
# * a pickle object 
# * a csv

# In[22]:


# df_APNews
df_APNews = pd.DataFrame(
    {'Article Date': list_dates,
     'Article Title': list_titles,
     'Article Link': list_links,
      'Article Content': news_contents})
     


# In[23]:


df_APNews


# In[15]:


#Save to pickle
df_APNews.to_pickle("./APNews.pkl")


# In[17]:


#Save to spreadsheet
df_APNews.to_csv("./APNews.csv")


# In[ ]:




