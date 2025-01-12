import os
import pandas as pd
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import models, transforms
from PIL import Image,ExifTags

def load_and_correct_image(image_path):
    # Open the image
    image = Image.open(image_path)
    
    # Try to apply the correct orientation from Exif metadata
    try:
        for orientation in ExifTags.TAGS.keys():
            if ExifTags.TAGS[orientation] == 'Orientation':
                break
        exif = image._getexif()
        if exif is not None:
            orientation_value = exif.get(orientation, None)
            if orientation_value == 3:
                image = image.rotate(180, expand=True)
            elif orientation_value == 6:
                image = image.rotate(270, expand=True)
            elif orientation_value == 8:
                image = image.rotate(90, expand=True)
    except Exception as e:
        print(f"Orientation correction failed: {e}")

    # Convert to RGB
    image = image.convert('RGB') #convert to RGB colour mode 
    return image

def load_image(image_path, max_size=400,shape=None):
    # Load an image and resize it to fit within the maximum size
    corrected_image=load_and_correct_image(image_path)

    # Handle shape (tuple) or size (int)
    if shape:  # If shape is provided, calculate size based on height and width
        height, width = shape
        scale = (max_size / max(height, width))
    else:  # Default to max dimension of the image
        size = max(corrected_image.size)
        scale = max_size / size
    transform = transforms.Compose([
        transforms.Resize((int(corrected_image.size[1] * scale), int(corrected_image.size[0] * scale))),
        transforms.ToTensor()
    ])
    image = transform(corrected_image).unsqueeze(0)  # Add batch dimension at position 0 
    return image


def save_image(tensor, output_path):
    image = tensor.cpu().clone().squeeze(0)  # Remove batch dimension
    image = transforms.ToPILImage()(image)
    image.save(output_path)
    print(f"Image saved to {output_path}")

def im_convert(tensor):
    image = tensor.to("cpu").clone().detach()
    image = image.numpy().squeeze() # removes all dimensions in the NumPy array that have a size of 1
    image = image.transpose(1, 2, 0) # Transpose to change the shape from (C, H, W) to (H, W, C) for visualization
    
    image = image.clip(0, 1)
    return image







