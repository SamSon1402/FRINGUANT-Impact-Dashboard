import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime, timedelta

def load_data():
    """Load or generate data for the dashboard"""
    processed_data_path = Path("data/processed/ecommerce_data.csv")
    
    # Check if processed data exists
    if processed_data_path.exists():
        return pd.read_csv(processed_data_path)
    else:
        # Generate sample data
        data = generate_sample_data()
        
        # Save processed data
        processed_data_path.parent.mkdir(parents=True, exist_ok=True)
        data.to_csv(processed_data_path, index=False)
        
        return data

def generate_sample_data(n_samples=1000):
    """Generate sample e-commerce data for demonstration"""
    np.random.seed(42)  # For reproducibility
    
    # Date range for the past year
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365)
    date_range = pd.date_range(start=start_date, end=end_date, periods=n_samples)
    
    # Product categories
    categories = ['Tops', 'Bottoms', 'Dresses', 'Outerwear', 'Activewear']
    
    # A/B test groups
    groups = ['Control', 'Size Recommendation']
    
    # Sample data structure
    data = {
        'date': np.random.choice(date_range, n_samples),
        'user_id': np.arange(1, n_samples + 1),
        'product_id': np.random.randint(1000, 10000, n_samples),
        'product_category': np.random.choice(categories, n_samples),
        'test_group': np.random.choice(groups, n_samples),
        'viewed': np.ones(n_samples),  # All products were viewed
        'added_to_cart': np.random.choice([0, 1], n_samples, p=[0.4, 0.6]),
        'purchased': np.zeros(n_samples),  # Will be filled conditionally
        'returned': np.zeros(n_samples),   # Will be filled conditionally
        'satisfaction_score': np.zeros(n_samples)  # Will be filled conditionally
    }
    
    # Create a DataFrame
    df = pd.DataFrame(data)
    
    # Conditional probabilities
    for i, row in df.iterrows():
        # Purchase probability higher with size recommendation
        if row['added_to_cart'] == 1:
            if row['test_group'] == 'Control':
                df.at[i, 'purchased'] = np.random.choice([0, 1], p=[0.4, 0.6])
            else:  # Size Recommendation group
                df.at[i, 'purchased'] = np.random.choice([0, 1], p=[0.25, 0.75])
        
        # Return probability lower with size recommendation
        if row['purchased'] == 1:
            if row['test_group'] == 'Control':
                df.at[i, 'returned'] = np.random.choice([0, 1], p=[0.8, 0.2])
            else:  # Size Recommendation group
                df.at[i, 'returned'] = np.random.choice([0, 1], p=[0.92, 0.08])
            
            # Satisfaction score higher with size recommendation and no returns
            if row['returned'] == 0:
                if row['test_group'] == 'Control':
                    df.at[i, 'satisfaction_score'] = np.random.randint(7, 10)
                else:  # Size Recommendation group
                    df.at[i, 'satisfaction_score'] = np.random.randint(8, 11)
            else:  # Returned items have lower satisfaction
                df.at[i, 'satisfaction_score'] = np.random.randint(1, 6)
    
    return df

def filter_data(df, category=None, date_range=None):
    """Filter data based on category and date range"""
    filtered_df = df.copy()
    
    if category and category != "All Categories":
        filtered_df = filtered_df[filtered_df['product_category'] == category]
    
    if date_range:
        start_date, end_date = date_range
        filtered_df = filtered_df[(filtered_df['date'] >= start_date) & 
                                 (filtered_df['date'] <= end_date)]
    
    return filtered_df