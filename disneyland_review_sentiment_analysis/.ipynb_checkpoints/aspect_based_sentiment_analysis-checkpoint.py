#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pandas as pd
import numpy as np
import os
from transformers import pipeline


from openai import OpenAI
from dotenv import load_dotenv

from sklearn.cluster import KMeans
import os
api_key = os.environ.get("OPENAI_API_KEY")



# In[12]:


review_df=pd.read_csv(os.path.join(os.getcwd(),'reviews_with_summaries.csv'))


# In[51]:


client = OpenAI()


# In[53]:


# Function to generate embeddings
def get_embedding(text,model="text-embedding-3-small"): 
    text = text.replace("\n", " ")  
    return client.embeddings.create(input = [text], model=model).data[0].embedding
    


# In[55]:


review_df['embedding'] = review_df['summary'].apply(lambda x: get_embedding(x, model='text-embedding-3-small'))


# In[99]:


review_df.head()


# In[ ]:


from sklearn.cluster import KMeans
import numpy as np
from sklearn.manifold import TSNE

# Extract embeddings as a NumPy array
embeddings = np.array(review_df['embedding'].tolist())

# Perform clustering
num_clusters = 3  # Adjust based on your dataset
kmeans = KMeans(n_clusters=num_clusters, random_state=42)
review_df['cluster'] = kmeans.fit_predict(embeddings)

# Display clustered DataFrame
print(review_df[['summary', 'cluster']])


# In[103]:


# Function to recommend reviews based on user input
def recommend_reviews(user_input, df, kmeans_model):
    # Generate embedding for user input
    user_embedding = get_embedding(user_input)
    
    # Predict the cluster for the user's input
    user_cluster = kmeans_model.predict([user_embedding])[0]
    
    # Get reviews from the same cluster
    recommendations = df[df['cluster'] == user_cluster]
    
    return recommendations[['review', 'summary']][:5]


# In[105]:




# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




