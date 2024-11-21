import pandas as pd
import numpy as np
import os
from transformers import pipeline

import joblib
from openai import OpenAI
from dotenv import load_dotenv

from sklearn.cluster import KMeans
import os

# Load precomputed data
review_df = pd.read_csv("precomputed_embeddings_with_clusters.csv")

# Convert embeddings back to NumPy arrays
review_df['embedding'] = review_df['embedding'].apply(eval)  # Convert string to list
embeddings = np.array(review_df['embedding'].tolist())

# Load precomputed KMeans model
kmeans = joblib.load("kmeans_model.pkl")

# Function to recommend reviews based on user input
def recommend_reviews(user_input, df, kmeans_model):
    # Generate embedding for user input
    user_embedding = get_embedding(user_input)
    
    # Predict the cluster for the user's input
    user_cluster = kmeans_model.predict([user_embedding])[0]
    
    # Get reviews from the same cluster
    recommendations = df[df['cluster'] == user_cluster]
    
    return recommendations[['review', 'summary']][:5]

