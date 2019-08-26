#!/usr/bin/env python
# coding: utf-8

# In[12]:


get_ipython().system('pip install wikipedia')


# In[9]:


from bs4 import BeautifulSoup as bs
import requests as req
import pandas as pd


# ### Downloading Data 

# In[10]:


url = "https://en.wikipedia.org/wiki/List_of_postal_codes_of_Canada:_M"
source = req.get(url).text
Canada_data = bs(source, 'lxml')


# ### Creating Dataframe

# In[11]:


column_names = ['Postalcode','Borough','Neighborhood']
toronto = pd.DataFrame(columns = column_names)


# ### Using Loop to  find the postalcode, borough &  neighborhood 

# In[12]:


content = Canada_data.find('div', class_='mw-parser-output')
table = content.table.tbody
postal_code = 0
borough = 0
neighborhood = 0

for tr in table.find_all('tr'):
    i = 0
    for td in tr.find_all('td'):
        if i == 0:
            postal_code = td.text
            i = i + 1
        elif i == 1:
            borough = td.text
            i = i + 1
        elif i == 2: 
            neighborhood = td.text.strip('\n').replace(']','')
    toronto = toronto.append({'Postalcode': postal_code,'Borough': borough,'Neighborhood': neighborhood},ignore_index=True)


# ### Cleaning Data

# In[13]:


toronto = toronto[toronto.Borough!='Not assigned']
toronto = toronto[toronto.Borough!= 0]
toronto.reset_index(drop = True, inplace = True)
i = 0
for i in range(0,toronto.shape[0]):
    if toronto.iloc[i][2] == 'Not assigned':
        toronto.iloc[i][2] = toronto.iloc[i][1]
        i = i+1
        
df = toronto.groupby(['Postalcode','Borough'])['Neighborhood'].apply(', '.join).reset_index()
df


# In[14]:


df = df.dropna()
empty = 'Not assigned'
df = df[(df.Postalcode != empty ) & (df.Borough != empty) & (df.Neighborhood != empty)]


# In[15]:


df


# In[16]:


def neighborhood_list(grouped):    
    return ', '.join(sorted(grouped['Neighborhood'].tolist()))
                    
test = df.groupby(['Postalcode', 'Borough'])
df_new = test.apply(neighborhood_list).reset_index(name='Neighborhood')


# In[17]:


print(df_new.shape)
df_new

