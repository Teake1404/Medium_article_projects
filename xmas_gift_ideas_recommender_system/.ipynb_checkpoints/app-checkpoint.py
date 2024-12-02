import streamlit as st
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import joblib

# Load your precomputed embeddings and dataset
df = pd.read_csv('df_with_embeddings.csv')  # Replace with the actual dataset
gift_embeddings = np.load('gift_embeddings.npy')  # Replace with the actual embeddings

@st.cache_resource
def load_model():
    return joblib.load("model.pkl")

model = load_model()

# Budget Filter
def is_within_budget(price_range, min_budget, max_budget):
    try:
        price_values = price_range.replace('£', '').split('-')
        if len(price_values) == 2:
            min_price, max_price = map(float, price_values)
        else:
            min_price = max_price = float(price_values[0])
        return min_price >= min_budget and max_price <= max_budget
    except Exception:
        return False

# Streamlit input fields
user_input = st.text_input("Enter a description of the recipient (e.g., 'Dad who loves tea')")
min_budget = st.slider("Min Budget (£)", min_value=0, max_value=1000, value=20)
max_budget = st.slider("Max Budget (£)", min_value=0, max_value=1000, value=100)

if user_input:
    # Generate user embedding for description (ensure you already have the model and embeddings)
    user_embedding = model.encode(user_input).reshape(1, -1)  # Replace 'model' with your preloaded model
    similarity_scores = cosine_similarity(user_embedding, gift_embeddings)

    # Apply budget filtering
    df['similarity_score'] = similarity_scores.flatten()
    filtered_df = df[df['Budget Range'].apply(lambda x: is_within_budget(x, min_budget, max_budget))]
    filtered_df_sorted = filtered_df.sort_values(by='similarity_score', ascending=False)

    # Get top N recommendations
    top_n = 5
    top_recommendations = filtered_df_sorted.head(top_n)

    # Display results
    st.write("Top Gift Recommendations:")
    st.write(top_recommendations[['Gift Idea', 'Persona','Description','Budget Range', 'similarity_score']])
