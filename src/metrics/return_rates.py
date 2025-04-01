import pandas as pd
import numpy as np

def calculate_return_metrics(df):
    """
    Calculate return rate metrics for both control and size recommendation groups
    
    Returns:
        dict: Dictionary containing return rate metrics
    """
    # Filter only purchased items
    purchased_df = df[df['purchased'] == 1]
    
    # Split data by test group
    control_df = purchased_df[purchased_df['test_group'] == 'Control']
    recommendation_df = purchased_df[purchased_df['test_group'] == 'Size Recommendation']
    
    # Calculate overall return rates
    if len(control_df) > 0:
        control_return_rate = (control_df['returned'].sum() / len(control_df)) * 100
    else:
        control_return_rate = 0
        
    if len(recommendation_df) > 0:
        recommendation_return_rate = (recommendation_df['returned'].sum() / len(recommendation_df)) * 100
    else:
        recommendation_return_rate = 0
    
    # Calculate reduction
    if control_return_rate > 0:
        return_rate_reduction = ((control_return_rate - recommendation_return_rate) / control_return_rate) * 100
    else:
        return_rate_reduction = 0
    
    # Compile metrics
    metrics = {
        'overall': {
            'control': control_return_rate,
            'recommendation': recommendation_return_rate,
            'reduction': return_rate_reduction
        }
    }
    
    return metrics

def calculate_return_by_category(df):
    """
    Calculate return rate metrics broken down by product category
    
    Returns:
        pd.DataFrame: DataFrame with return rate metrics by category
    """
    # Filter only purchased items
    purchased_df = df[df['purchased'] == 1]
    
    categories = purchased_df['product_category'].unique()
    results = []
    
    for category in categories:
        category_df = purchased_df[purchased_df['product_category'] == category]
        
        # Split by test group
        control_df = category_df[category_df['test_group'] == 'Control']
        recommendation_df = category_df[category_df['test_group'] == 'Size Recommendation']
        
        # Calculate return rates for each group
        if len(control_df) > 0:
            control_return_rate = (control_df['returned'].sum() / len(control_df)) * 100
        else:
            control_return_rate = 0
            
        if len(recommendation_df) > 0:
            recommendation_return_rate = (recommendation_df['returned'].sum() / len(recommendation_df)) * 100
        else:
            recommendation_return_rate = 0
            
        # Calculate reduction
        if control_return_rate > 0:
            reduction = ((control_return_rate - recommendation_return_rate) / control_return_rate) * 100
        else:
            reduction = 0
            
        results.append({
            'category': category,
            'control_return_rate': control_return_rate,
            'recommendation_return_rate': recommendation_return_rate,
            'reduction': reduction
        })
    
    return pd.DataFrame(results)

def calculate_return_cost_savings(df, average_return_cost=15):
    """
    Calculate cost savings from reduced returns
    
    Args:
        df: DataFrame with e-commerce data
        average_return_cost: Average cost to process a return in dollars
        
    Returns:
        float: Estimated cost savings
    """
    # Filter only purchased items
    purchased_df = df[df['purchased'] == 1]
    
    # Split data by test group
    control_df = purchased_df[purchased_df['test_group'] == 'Control']
    recommendation_df = purchased_df[purchased_df['test_group'] == 'Size Recommendation']
    
    # Calculate return counts
    control_returns = control_df['returned'].sum()
    recommendation_returns = recommendation_df['returned'].sum()
    
    # Normalize by group size
    control_size = len(control_df)
    recommendation_size = len(recommendation_df)
    
    if control_size > 0 and recommendation_size > 0:
        # Calculate return rate difference
        control_return_rate = control_returns / control_size
        recommendation_return_rate = recommendation_returns / recommendation_size
        
        # Estimate number of avoided returns
        avoided_returns = recommendation_size * (control_return_rate - recommendation_return_rate)
        
        # Calculate savings
        savings = avoided_returns * average_return_cost
    else:
        savings = 0
    
    return savings