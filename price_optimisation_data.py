import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objs as go
import plotly.io as pio
pio.renderers.default = 'iframe'
pd.set_option('display.max_columns', None)
import statsmodels.api as sm
from statsmodels.tools.tools import add_constant
from statsmodels.nonparametric.smoothers_lowess import lowess
from pygam import ExpectileGAM


def plot_revenue_gam_results_using_lowess(df):
    # Scatter plot with unit_price vs qty and color by product_category_name
    fig = px.scatter(df, 
                     x='unit_price', 
                     y='total_price', 
                     color='product_category_name', 
                     labels={'unit_price': 'Unit Price', 'total_price': 'Actual Revenue'},
                     title="Revenue vs Unit Price with GAM Predictions")
    
    # Add smooth prediction lines and ribbons
    for category in df['product_category_name'].unique():
        category_data = df[df['product_category_name'] == category]
        
        # Smooth the median prediction (pred_0.5)
        x_smooth, y_smooth = smooth_prediction(category_data['unit_price'], category_data['revenue_pred_0.5'])
        fig.add_traces(go.Scatter(x=x_smooth, y=y_smooth, mode='lines', name=f'{category} Median Prediction', line=dict(color='blue')))
    
        # Smooth lower and upper bounds for ribbon
        x_smooth_low, y_smooth_low = smooth_prediction(category_data['unit_price'], category_data['revenue_pred_0.025'])
        x_smooth_high, y_smooth_high = smooth_prediction(category_data['unit_price'], category_data['revenue_pred_0.975'])
    
        # Add ribbon for prediction intervals using go.Scatter with 'fill'
        fig.add_traces(go.Scatter(
            x=np.concatenate([x_smooth, x_smooth[::-1]]),  # Concatenate x for filling the area
            y=np.concatenate([y_smooth_high, y_smooth_low[::-1]]),  # Concatenate y for filling the area
            fill='toself',
            fillcolor='rgba(211, 211, 211, 0.5)',  # Light gray fill color with transparency
            line=dict(color='rgba(255,255,255,0)'),  # No visible line
            showlegend=False,
            name=f'{category} Prediction Interval'
        ))          
    # Show plot
    return fig.show()
    
# Function to smooth prediction lines using lowess
def smooth_prediction(x, y):
    lowess_result = lowess(y, x, frac=0.3)
    return lowess_result[:, 0], lowess_result[:, 1]


def plot_gam_results_using_lowess(df):
    # Scatter plot with unit_price vs qty and color by product_category_name
    fig = px.scatter(df, 
                     x='unit_price', 
                     y='qty', 
                     color='product_category_name', 
                     labels={'unit_price': 'Unit Price', 'qty': 'Quantity'},
                     title="Quantity vs Unit Price with GAM Predictions")
    
    # Add smooth prediction lines and ribbons
    for category in df['product_category_name'].unique():
        category_data = df[df['product_category_name'] == category]
        
        # Smooth the median prediction (pred_0.5)
        x_smooth, y_smooth = smooth_prediction(category_data['unit_price'], category_data['pred_0.5'])
        fig.add_traces(go.Scatter(x=x_smooth, y=y_smooth, mode='lines', name=f'{category} Median Prediction', line=dict(color='blue')))
    
        # Smooth lower and upper bounds for ribbon
        x_smooth_low, y_smooth_low = smooth_prediction(category_data['unit_price'], category_data['pred_0.025'])
        x_smooth_high, y_smooth_high = smooth_prediction(category_data['unit_price'], category_data['pred_0.975'])
    
        # Add ribbon for prediction intervals using go.Scatter with 'fill'
        fig.add_traces(go.Scatter(
            x=np.concatenate([x_smooth, x_smooth[::-1]]),  # Concatenate x for filling the area
            y=np.concatenate([y_smooth_high, y_smooth_low[::-1]]),  # Concatenate y for filling the area
            fill='toself',
            fillcolor='rgba(211, 211, 211, 0.5)',  # Light gray fill color with transparency
            line=dict(color='rgba(255,255,255,0)'),  # No visible line
            showlegend=False,
            name=f'{category} Prediction Interval'
        ))
        
            
    # Show plot
    return fig.show()

def plot_gam_one_product_using_lowess(df, category):
    # Scatter plot with unit_price vs qty and color by product_category_name
    category_data = df[df['product_category_name'] == category]
    fig = px.scatter(category_data, 
                     x='unit_price', 
                     y='qty', 
                     color='product_category_name', 
                     labels={'unit_price': 'Unit Price', 'qty': 'Quantity'},
                     title="Quantity vs Unit Price with GAM Predictions")
    
    # Add smooth prediction lines and ribbonsfor category in df['product_category_name'].unique():
    
    # Smooth the median prediction (pred_0.5)
    x_smooth, y_smooth = smooth_prediction(category_data['unit_price'], category_data['pred_0.5'])
    fig.add_traces(go.Scatter(x=x_smooth, y=y_smooth, mode='lines', name=f'{category} Median Prediction', line=dict(color='blue')))

    # Smooth lower and upper bounds for ribbon
    x_smooth_low, y_smooth_low = smooth_prediction(category_data['unit_price'], category_data['pred_0.025'])
    x_smooth_high, y_smooth_high = smooth_prediction(category_data['unit_price'], category_data['pred_0.975'])

    # Add ribbon for prediction intervals using go.Scatter with 'fill'
    fig.add_traces(go.Scatter(
        x=np.concatenate([x_smooth, x_smooth[::-1]]),  # Concatenate x for filling the area
        y=np.concatenate([y_smooth_high, y_smooth_low[::-1]]),  # Concatenate y for filling the area
        fill='toself',
        fillcolor='rgba(211, 211, 211, 0.5)',  # Light gray fill color with transparency
        line=dict(color='rgba(255,255,255,0)'),  # No visible line
        showlegend=False,
        name=f'{category} Prediction Interval'
    ))
        
            
    # Show plot
    return fig.show()
def plot_revenue_gam_one_product_using_lowess(df,category):
    # Scatter plot with unit_price vs qty and color by product_category_name
    category_data = df[df['product_category_name'] == category]
    fig = px.scatter(category_data, 
                     x='unit_price', 
                     y='total_price', 
                     color='product_category_name', 
                     labels={'unit_price': 'Unit Price', 'total_price': 'Actual Revenue'},
                     title="Revenue vs Unit Price with GAM Predictions")
    
    # Add smooth prediction lines and ribbons
           
    # Smooth the median prediction (pred_0.5)
    x_smooth, y_smooth = smooth_prediction(category_data['unit_price'], category_data['revenue_pred_0.5'])
    fig.add_traces(go.Scatter(x=x_smooth, y=y_smooth, mode='lines', name=f'{category} Median Prediction', line=dict(color='blue')))

    # Smooth lower and upper bounds for ribbon
    x_smooth_low, y_smooth_low = smooth_prediction(category_data['unit_price'], category_data['revenue_pred_0.025'])
    x_smooth_high, y_smooth_high = smooth_prediction(category_data['unit_price'], category_data['revenue_pred_0.975'])

    # Add ribbon for prediction intervals using go.Scatter with 'fill'
    fig.add_traces(go.Scatter(
        x=np.concatenate([x_smooth, x_smooth[::-1]]),  # Concatenate x for filling the area
        y=np.concatenate([y_smooth_high, y_smooth_low[::-1]]),  # Concatenate y for filling the area
        fill='toself',
        fillcolor='rgba(211, 211, 211, 0.5)',  # Light gray fill color with transparency
        line=dict(color='rgba(255,255,255,0)'),  # No visible line
        showlegend=False,
        name=f'{category} Prediction Interval'
    ))          
    # Show plot
    return fig.show()