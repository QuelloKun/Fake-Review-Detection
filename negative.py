#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np 
import pickle
import itertools
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import PassiveAggressiveClassifier
from sklearn.metrics import accuracy_score, confusion_matrix


# In[2]:


train = pd.read_csv('review.csv')


# In[3]:


train


# In[4]:


train.drop(columns=['source','sentiment','id'],inplace=True)


# In[5]:


#train=train.dropna()


# In[6]:


train


# In[7]:


df_x=train['review']
df_y=train['prediction']


# In[8]:


from sklearn.model_selection import train_test_split
x_train, x_test, y_train, y_test = train_test_split(df_x,df_y,test_size=0.3, random_state=9)
print(x_train.shape)
print(x_test.shape)


# In[9]:


tfidf_vectorizer = TfidfVectorizer(stop_words='english', max_df=0.7)


# In[10]:


from sklearn.feature_extraction.text import TfidfVectorizer
tfidf_vectorizer= TfidfVectorizer(min_df=1,stop_words='english')


# In[11]:


tfidf_train = tfidf_vectorizer.fit_transform(x_train) 
X_test_counts=tfidf_vectorizer.transform(x_test)


# In[12]:


pac = PassiveAggressiveClassifier(max_iter=50)
pac.fit(tfidf_train,y_train)


# In[13]:


#pac.score(tfidf_train,y_train)


# In[14]:


#from sklearn.metrics import accuracy_score
#y_pred = pac.predict(X_test_counts)
#accuracy_score(y_pred,y_test)


# In[15]:


#docs_new=['Gutes Hotel zu fairem Preis in der Stadtmitte Chicagos, kann ohne Vorbehalt empfohlen werden!']
#X_new_counts=tfidf_vectorizer.transform(docs_new)
#X_new_tfidf=tfidf_transformer.fit_transform(X_new_counts)
#predicted=pac.predict(X_new_counts)
#predicted[0]


# In[16]:


with open('tfid.pickle','wb') as f:
    pickle.dump(tfidf_vectorizer,f)


# In[17]:


with open('model_fakenews.pickle','wb') as f:
    pickle.dump(pac,f)


# In[ ]:




