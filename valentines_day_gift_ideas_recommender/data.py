import pandas as pd
import numpy as np
import re
import plotly.express as px
import plotly.graph_objects as go
pd.set_option('display.max_columns',None)
pd.set_option('display.max_rows',None)
import cv2
from deepface import DeepFace
import os
import tensorflow as tf
import tensorflow_hub as hub
import matplotlib.pyplot as plt
from mtcnn import MTCNN



def detect_faces(image_path):
    # Load the pre-trained Haar Cascade model
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    
    # Read the image and convert to grayscale
    image = cv2.imread(image_path)
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # Convert to grayscale for face detection
    
    # # Detect faces in the image
    # faces = face_cascade.detectMultiScale(gray_image, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    # Initialize MTCNN detector
    detector = MTCNN()
    
    # Detect faces
    faces = detector.detect_faces(image)
    
    # Draw rectangles around detected faces
    for face in faces:
        x, y, w, h = face['box']
        cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 6)  # Green rectangle with thickness of 6
        
    # Display the image with detected faces
    plt.imshow(image)  # Convert BGR to RGB for display
    plt.title("Detected Faces (MTCNN)")
    plt.axis("off")
    plt.show()
    
    return faces, image
    
def analyze_mood(image_path):
    # Analyze facial expressions using DeepFace
    result = DeepFace.analyze(img_path=image_path, actions=['emotion'], enforce_detection=False)
    dominant_emotion = result[0]['dominant_emotion']
    print(f"Detected emotion: {dominant_emotion}")
    return dominant_emotion
def add_elements(output_path, style_path, x_value,y_value):
        # Load the original image (after style transfer)
    original_image = cv2.imread(output_path)
    
    # Load the heart shape image (ensure it's a PNG with transparency)
    heart_image = cv2.imread(style_path, cv2.IMREAD_UNCHANGED)  # Load with alpha channel
    
    # Resize the heart to fit the original image size or adjust as necessary
    heart_resized = cv2.resize(heart_image, (50, 50))  # Resize heart (adjust the size as needed)
    
    # Extract the alpha channel (transparency) from the heart image
    alpha_channel = heart_resized[:, :, 3] / 255.0  # Normalize alpha to [0,1]
    heart_rgb = heart_resized[:, :, :3]
    
    # Determine the position for the heart overlay (top-left corner of the blue lines)
    x, y = x_value, y_value  # Adjust these values to place the heart over the blue lines
    
    # Get the region of interest (ROI) where we will place the heart
    roi = original_image[y:y+heart_resized.shape[0], x:x+heart_resized.shape[1]]
    
    # Blend the heart onto the ROI
    for c in range(0, 3):
        roi[:, :, c] = (1. - alpha_channel) * roi[:, :, c] + alpha_channel * heart_rgb[:, :, c]
    
    # Place the heart image back into the original image
    original_image[y:y+heart_resized.shape[0], x:x+heart_resized.shape[1]] = roi
    return original_image

def split_message_in_lies(message):
    generated_message=message.split(':')[1]

    message_list=generated_message.split('.')
    # Iterate over the lines, excluding the last one
    for i in range(len(message_list) - 1):  # Exclude last item
        message_dict[f'line_{i}'] = message_list[i].strip()  # Use strip() to clean up any extra spaces
    
    return message_dict
