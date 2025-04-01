import pandas as pd
import numpy as np

def calculate_satisfaction_metrics(df):
    """
    Calculate customer satisfaction metrics for both control and size recommendation groups
    
    Returns:
        dict: Dictionary containing satisfaction metrics
    """
    # Filter only purchased items with satisfaction scores
    purchased_df = df[(df['purchased'] == 1) & (df['satisfaction_score'] > 0)]
    
    # Split data by test group
    control_df = purchased_df[purchased_df['test_group'] == 'Control']
    recommendation_df = purchased_df[purchased_df['test_group'] == 'Size Recommendation']
    
    # Calculate average satisfaction scores
    if len(control_df) > 0:
        control_satisfaction = control_df['satisfaction_score'].mean()
    else:
        control_satisfaction = 0
        
    if len(recommendation_df) > 0:
        recommendation_satisfaction = recommendation_df['satisfaction_score'].mean()
    else:
        recommendation_satisfaction = 0
    
    # Calculate improvement
    if control_satisfaction > 0:
        satisfaction_improvement = ((recommendation_satisfaction - control_satisfaction) / control_satisfaction) * 100
    else:
        satisfaction_improvement = 0
    
    # Compile metrics
    metrics = {
        'overall': {
            'control': control_satisfaction,
            'recommendation': recommendation_satisfaction,
            'improvement': satisfaction_improvement
        }
    }
    
    return metrics

def calculate_satisfaction_by_category(df):
    """
    Calculate satisfaction metrics broken down by product category
    
    Returns:
        pd.DataFrame: DataFrame with satisfaction metrics by category
    """
    # Filter only purchased items with satisfaction scores
    purchased_df = df[(df['purchased'] == 1) & (df['satisfaction_score'] > 0)]
    
    categories = purchased_df['product_category'].unique()
    results = []
    
    for category in categories:
        category_df = purchased_df[purchased_df['product_category'] == category]
        
        # Split by test group
        control_df = category_df[category_df['test_group'] == 'Control']
        recommendation_df = category_df[category_df['test_group'] == 'Size Recommendation']
        
        # Calculate satisfaction for each group
        if len(control_df) > 0:
            control_satisfaction = control_df['satisfaction_score'].mean()
        else:
            control_satisfaction = 0
            
        if len(recommendation_df) > 0:
            recommendation_satisfaction = recommendation_df['satisfaction_score'].mean()
        else:
            recommendation_satisfaction = 0
            
        # Calculate improvement
        if control_satisfaction > 0:
            improvement = ((recommendation_satisfaction - control_satisfaction) / control_satisfaction) * 100
        else:
            improvement = 0
            
        results.append({
            'category': category,
            'control_satisfaction': control_satisfaction,
            'recommendation_satisfaction': recommendation_satisfaction,
            'improvement': improvement
        })
    
    return pd.DataFrame(results)

def calculate_nps_distribution(df):
    """
    Calculate NPS distribution based on satisfaction scores
    
    Returns:
        dict: Dictionary containing NPS metrics
    """
    # Filter only purchased items with satisfaction scores
    purchased_df = df[(df['purchased'] == 1) & (df['satisfaction_score'] > 0)]
    
    # Map satisfaction scores to NPS categories
    def map_to_nps(score):
        if score >= 9:  # Promoters
            return 'Promoter'
        elif score >= 7:  # Passives
            return 'Passive'
        else:  # Detractors
            return 'Detractor'
    
    purchased_df['nps_category'] = purchased_df['satisfaction_score'].apply(map_to_nps)
    
    # Calculate NPS for each test group
    nps_by_group = {}
    
    for group in ['Control', 'Size Recommendation']:
        group_df = purchased_df[purchased_df['test_group'] == group]
        
        if len(group_df) > 0:
            promoters = (group_df['nps_category'] == 'Promoter').sum() / len(group_df) * 100
            detractors = (group_df['nps_category'] == 'Detractor').sum() / len(group_df) * 100
            nps = promoters - detractors
        else:
            promoters = 0
            detractors = 0
            nps = 0
            
        nps_by_group[group] = {
            'promoters': promoters,
            'detractors': detractors,
            'nps_score': nps
        }
    
    return nps_by_group