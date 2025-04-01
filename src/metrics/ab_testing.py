import pandas as pd
import numpy as np
import scipy.stats as stats

def perform_conversion_ab_test(df):
    """
    Perform A/B test analysis on conversion rates
    
    Returns:
        dict: Dictionary containing A/B test results
    """
    # Split data by test group
    control_df = df[df['test_group'] == 'Control']
    treatment_df = df[df['test_group'] == 'Size Recommendation']
    
    # Get conversion counts for each group
    control_conversions = control_df['purchased'].sum()
    control_trials = len(control_df)
    
    treatment_conversions = treatment_df['purchased'].sum()
    treatment_trials = len(treatment_df)
    
    # Calculate conversion rates
    control_rate = control_conversions / control_trials if control_trials > 0 else 0
    treatment_rate = treatment_conversions / treatment_trials if treatment_trials > 0 else 0
    
    # Perform z-test for proportions
    if control_trials > 0 and treatment_trials > 0:
        z_stat, p_value = stats.proportions_ztest(
            [treatment_conversions, control_conversions],
            [treatment_trials, control_trials]
        )
        
        # Determine statistical significance (alpha = 0.05)
        is_significant = p_value < 0.05
        
        # Calculate relative lift
        relative_lift = ((treatment_rate - control_rate) / control_rate) * 100
    else:
        z_stat = 0
        p_value = 1
        is_significant = False
        relative_lift = 0
    
    # Compile results
    results = {
        'control_rate': control_rate * 100,  # Convert to percentage
        'treatment_rate': treatment_rate * 100,  # Convert to percentage
        'absolute_difference': (treatment_rate - control_rate) * 100,  # Convert to percentage
        'relative_lift': relative_lift,
        'p_value': p_value,
        'is_significant': is_significant,
        'confidence': (1 - p_value) * 100 if p_value < 1 else 0  # Confidence level
    }
    
    return results

def perform_return_rate_ab_test(df):
    """
    Perform A/B test analysis on return rates
    
    Returns:
        dict: Dictionary containing A/B test results
    """
    # Filter only purchased items
    purchased_df = df[df['purchased'] == 1]
    
    # Split data by test group
    control_df = purchased_df[purchased_df['test_group'] == 'Control']
    treatment_df = purchased_df[purchased_df['test_group'] == 'Size Recommendation']
    
    # Get return counts for each group
    control_returns = control_df['returned'].sum()
    control_trials = len(control_df)
    
    treatment_returns = treatment_df['returned'].sum()
    treatment_trials = len(treatment_df)
    
    # Calculate return rates
    control_rate = control_returns / control_trials if control_trials > 0 else 0
    treatment_rate = treatment_returns / treatment_trials if treatment_trials > 0 else 0
    
    # Perform z-test for proportions
    if control_trials > 0 and treatment_trials > 0:
        z_stat, p_value = stats.proportions_ztest(
            [treatment_returns, control_returns],
            [treatment_trials, control_trials]
        )
        
        # Determine statistical significance (alpha = 0.05)
        is_significant = p_value < 0.05
        
        # Calculate relative reduction
        relative_reduction = ((control_rate - treatment_rate) / control_rate) * 100 if control_rate > 0 else 0
    else:
        z_stat = 0
        p_value = 1
        is_significant = False
        relative_reduction = 0
    
    # Compile results
    results = {
        'control_rate': control_rate * 100,  # Convert to percentage
        'treatment_rate': treatment_rate * 100,  # Convert to percentage
        'absolute_difference': (control_rate - treatment_rate) * 100,  # Convert to percentage
        'relative_reduction': relative_reduction,
        'p_value': p_value,
        'is_significant': is_significant,
        'confidence': (1 - p_value) * 100 if p_value < 1 else 0  # Confidence level
    }
    
    return results

def perform_satisfaction_ab_test(df):
    """
    Perform A/B test analysis on satisfaction scores
    
    Returns:
        dict: Dictionary containing A/B test results
    """
    # Filter only purchased items with satisfaction scores
    purchased_df = df[(df['purchased'] == 1) & (df['satisfaction_score'] > 0)]
    
    # Split data by test group
    control_scores = purchased_df[purchased_df['test_group'] == 'Control']['satisfaction_score']
    treatment_scores = purchased_df[purchased_df['test_group'] == 'Size Recommendation']['satisfaction_score']
    
    # Calculate mean scores
    control_mean = control_scores.mean() if len(control_scores) > 0 else 0
    treatment_mean = treatment_scores.mean() if len(treatment_scores) > 0 else 0
    
    # Perform t-test for independent samples
    if len(control_scores) > 0 and len(treatment_scores) > 0:
        t_stat, p_value = stats.ttest_ind(treatment_scores, control_scores, equal_var=False)
        
        # Determine statistical significance (alpha = 0.05)
        is_significant = p_value < 0.05
        
        # Calculate relative improvement
        relative_improvement = ((treatment_mean - control_mean) / control_mean) * 100 if control_mean > 0 else 0
    else:
        t_stat = 0
        p_value = 1
        is_significant = False
        relative_improvement = 0
    
    # Compile results
    results = {
        'control_mean': control_mean,
        'treatment_mean': treatment_mean,
        'absolute_difference': treatment_mean - control_mean,
        'relative_improvement': relative_improvement,
        'p_value': p_value,
        'is_significant': is_significant,
        'confidence': (1 - p_value) * 100 if p_value < 1 else 0  # Confidence level
    }
    
    return results