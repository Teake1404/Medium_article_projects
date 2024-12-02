import streamlit as st
import pandas as pd
import numpy as np
import joblib

# Load your precomputed embeddings and dataset
df_sorted= pd.read_csv('df_sorted.csv')
user_item_matrix = pd.read_csv('updated_nan_user_item_matrix.csv')



@st.cache_resource
def load_model():
    return joblib.load("svd_model.pkl")

svd = load_model()

def recommend_gifts(user_id, model, df, top_n=5):
    """
    Recommend top N gifts for a specific user based on collaborative filtering.
    """
    # Get all gift ideas
    all_gifts = df.columns.tolist()
    
    # Gifts the user has already rated
    rated_gifts = user_item_matrix.loc[user_id].dropna().index.tolist()

    # Predict ratings for unrated gifts
    predictions = [
        (gift, model.predict(user_id, gift).est)
        for gift in all_gifts
        if gift not in rated_gifts
    ]

    # Sort by predicted ratings in descending order
    predictions.sort(key=lambda x: x[1], reverse=True)

    # Return top N recommendations
    return pd.DataFrame(predictions[:top_n], columns=["Gift Idea", "Predicted Rating"])

def hybrid_recommendations(user_input, user_id, model, content_scores, top_n=5):
    """
    Combine content-based and collaborative filtering for hybrid recommendations.
    """
    collaborative_recs = recommend_gifts(user_id, model, user_item_matrix)
    collaborative_scores = collaborative_recs.set_index('Gift Idea')['Predicted Rating']

    # Merge collaborative scores with content-based scores
    combined_scores = content_scores.copy()
    combined_scores['Collaborative Score'] = combined_scores['Gift Idea'].map(collaborative_scores)
    combined_scores['Hybrid Score'] = 0.5 * combined_scores['similarity_score'] + 0.5 * combined_scores['Collaborative Score']
    
    # Sort by hybrid score
    combined_scores = combined_scores.sort_values(by='Hybrid Score', ascending=False)
    return combined_scores[['Gift Idea', 'Persona', 'Description', 'Hybrid Score']].head(top_n)

# Get content-based scores
content_scores = df_sorted.copy()

user_input='2 year old toddler who loves animals'

# Example usage
hybrid_recs = hybrid_recommendations(user_input, 0, svd, content_scores, top_n=5)
st.write(hybrid_recs)

# Add User ID input
user_id = st.selectbox("Select a User ID", user_item_matrix.index.tolist())

# Add a button to generate recommendations
if st.button("Get Hybrid Recommendations"):
    hybrid_recs = hybrid_recommendations(user_input, user_id, svd, content_scores, top_n=5)
    st.write("Top Hybrid Recommendations:")
    st.write(hybrid_recs)

