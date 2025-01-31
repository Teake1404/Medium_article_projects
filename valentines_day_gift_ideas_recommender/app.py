import streamlit as st
from PIL import Image

# Step 1: Set the page configuration
st.set_page_config(page_title="Valentine's Day Card", page_icon="❤️", layout="wide")

# Step 2: Display the Title
st.title("Create Your Personalized Valentine's Day Card ❤️")

# Step 3: Let users upload a background image (optional)
st.sidebar.header("Upload a Custom Background (Optional)")
uploaded_background = st.sidebar.file_uploader("Choose a background image", type=["jpg", "jpeg", "png"])

# Step 4: Let users customize the text message (optional)
st.sidebar.header("Customize Your Message")
message = st.sidebar.text_area("Write your personalized message for the card:")

# Step 5: Display the default image or user-uploaded image
if uploaded_background is not None:
    # Open and display the uploaded background image
    background_image = Image.open(uploaded_background)
    st.image(background_image, caption="Your Custom Background", use_column_width=True)
else:
    # Default card image
    st.image('final_valentines_card_centered.jpg', caption="Your Valentine's Day Card", use_column_width=True)

# Step 6: Display the customizable message preview
if message:
    st.subheader("Preview Your Message")
    st.write(message)

# Step 7: Download Button for the Final Card
st.sidebar.header("Download Your Card")
st.sidebar.write("Click the button below to download your final card.")

# Here, you can implement the logic to allow users to modify the image (e.g., adding text dynamically, etc.)
# For now, we'll allow them to download the current version of the card
st.sidebar.download_button(
    label="Download Card",
    data=open('final_valentines_card_centered.jpg', 'rb').read(),
    file_name="final_valentines_card_centered.jpg",
    mime="image/jpeg"
)

# Step 8: Show the final result (could be the one generated from previous steps or uploaded by the user)
st.subheader("Final Result")
st.image('final_valentines_card_centered.jpg', caption="Your Valentine's Day Card", use_column_width=True)
