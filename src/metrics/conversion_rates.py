import pandas as pd
import numpy as np

def calculate_conversion_metrics(df):
    """
    Calculate conversion metrics for both control and size recommendation groups
    
    Returns:
        dict: Dictionary containing conversion metrics
    """
    # Split data by test group
    control_df = df[df['test_group'] == 'Control']
    recommendation_df = df[df['test_group'] == 'Size Recommendation']
    
    # Calculate view-to-cart conversion rates
    control_view_to_cart = (control_df['added_to_cart'].sum() / control_df['viewed'].sum()) * 100
    recommendation_view_to_cart = (recommendation_df['added_to_cart'].sum() / recommendation_df['viewed'].sum()) * 100
    view_to_cart_improvement = ((recommendation_view_to_cart - control_view_to_cart) / control_view_to_cart) * 100
    
    # Calculate cart-to-purchase conversion rates
    control_cart_to_purchase = (control_df[control_df['added_to_cart'] == 1]['purchased'].sum() / 
                              control_df['added_to_cart'].sum()) * 100
    recommendation_cart_to_purchase = (recommendation_df[recommendation_df['added_to_cart'] == 1]['purchased'].sum() / 
                                    recommendation_df['added_to_cart'].sum()) * 100
    cart_to_purchase_improvement = ((recommendation_cart_to_purchase - control_cart_to_purchase) / 
                                  control_cart_to_purchase) * 100
    
    # Calculate overall conversion rates (view-to-purchase)
    control_overall = (control_df['purchased'].sum() / control_df['viewed'].sum()) * 100
    recommendation_overall = (recommendation_df['purchased'].sum() / recommendation_df['viewed'].sum()) * 100
    overall_improvement = ((recommendation_overall - control_overall) / control_overall) * 100
    
    # Compile metrics
    metrics = {
        'view_to_cart': {
            'control': control_view_to_cart,
            'recommendation': recommendation_view_to_cart,
            'improvement': view_to_cart_improvement
        },
        'cart_to_purchase': {
            'control': control_cart_to_purchase,
            'recommendation': recommendation_cart_to_purchase,
            'improvement': cart_to_purchase_improvement
        },
        'overall': {
            'control': control_overall,
            'recommendation': recommendation_overall,
            'improvement': overall_improvement
        }
    }
    
    return metrics

def calculate_conversion_by_category(df):
    """
    Calculate conversion metrics broken down by product category
    
    Returns:
        pd.DataFrame: DataFrame with conversion metrics by category
    """
    categories = df['product_category'].unique()
    results = []
    
    for category in categories:
        category_df = df[df['product_category'] == category]
        
        # Split by test group
        control_df = category_df[category_df['test_group'] == 'Control']
        recommendation_df = category_df[category_df['test_group'] == 'Size Recommendation']
        
        # Calculate overall conversion for each group
        if len(control_df) > 0:
            control_conversion = (control_df['purchased'].sum() / control_df['viewed'].sum()) * 100
        else:
            control_conversion = 0
            
        if len(recommendation_df) > 0:
            recommendation_conversion = (recommendation_df['purchased'].sum() / recommendation_df['viewed'].sum()) * 100
        else:
            recommendation_conversion = 0
            
        # Calculate improvement
        if control_conversion > 0:
            improvement = ((recommendation_conversion - control_conversion) / control_conversion) * 100
        else:
            improvement = 0
            
        results.append({
            'category': category,
            'control_conversion': control_conversion,
            'recommendation_conversion': recommendation_conversion,
            'improvement': improvement
        })
    
    return pd.DataFrame(results)