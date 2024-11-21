from aspect_based_sentiment_analysis import *
import streamlit as st
import pandas as pd
import numpy as np
import joblib


# Load environment variables
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("API key not found. Set OPENAI_API_KEY in the .env file.")

# Initialize OpenAI client
client = OpenAI(api_key=api_key)


# Function to generate embeddings
def get_embedding(text,model="text-embedding-3-small"): 
    text = text.replace("\n", " ")  
    return client.embeddings.create(input = [text], model=model).data[0].embedding


# Load precomputed data
@st.cache_data
def load_precomputed_data():
    df = pd.read_csv("precomputed_embeddings_with_clusters.csv")
    df['embedding'] = df['embedding'].apply(eval)  # Convert string to list
    return df

@st.cache_resource
def load_kmeans_model():
    return joblib.load("kmeans_model.pkl")

review_df = load_precomputed_data()
kmeans = load_kmeans_model()

# Recommendation function
def recommend_reviews(user_input, df, kmeans_model):
    embedding = get_embedding(user_input)
    cluster = kmeans_model.predict([embedding])[0]
    recommendations = df[df['cluster'] == cluster]
    return recommendations[['review', 'summary']][:5]

# Streamlit UI
st.title("Review Recommendation System")
user_input = st.text_input("Enter your preferences (e.g., thrilling rides, friendly staff):")

if user_input:
    recommendations = recommend_reviews(user_input, review_df, kmeans)
    st.write("### Recommended Reviews")
    st.write(recommendations)

