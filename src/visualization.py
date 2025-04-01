import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np

# Color palette inspired by the monochromatic aesthetic
COLORS = {
    'primary': '#d0d0d0',    # Light gray
    'secondary': '#808080',  # Medium gray
    'accent': '#ffffff',     # White
    'background': '#101010', # Near black
    'positive': '#a0e4b0',   # Muted green
    'negative': '#e4a0a0'    # Muted red
}

def create_conversion_chart(df):
    """Create conversion rate chart comparing control vs recommendation groups"""
    # Calculate conversion rates
    control_df = df[df['test_group'] == 'Control']
    rec_df = df[df['test_group'] == 'Size Recommendation']
    
    control_view_to_cart = control_df['added_to_cart'].mean() * 100
    control_cart_to_purchase = control_df[control_df['added_to_cart'] == 1]['purchased'].mean() * 100
    control_overall = control_df['purchased'].mean() * 100
    
    rec_view_to_cart = rec_df['added_to_cart'].mean() * 100
    rec_cart_to_purchase = rec_df[rec_df['added_to_cart'] == 1]['purchased'].mean() * 100
    rec_overall = rec_df['purchased'].mean() * 100
    
    # Create the figure
    fig = go.Figure()
    
    # Add bars for control group
    fig.add_trace(go.Bar(
        x=['View to Cart', 'Cart to Purchase', 'Overall Conversion'],
        y=[control_view_to_cart, control_cart_to_purchase, control_overall],
        name='Control',
        marker_color=COLORS['secondary']
    ))
    
    # Add bars for recommendation group
    fig.add_trace(go.Bar(
        x=['View to Cart', 'Cart to Purchase', 'Overall Conversion'],
        y=[rec_view_to_cart, rec_cart_to_purchase, rec_overall],
        name='Size Recommendation',
        marker_color=COLORS['primary']
    ))
    
    # Calculate and display improvement percentages
    improvements = [
        (rec_view_to_cart - control_view_to_cart) / control_view_to_cart * 100,
        (rec_cart_to_purchase - control_cart_to_purchase) / control_cart_to_purchase * 100,
        (rec_overall - control_overall) / control_overall * 100
    ]
    
    for i, (x, y, imp) in enumerate(zip(
        ['View to Cart', 'Cart to Purchase', 'Overall Conversion'],
        [rec_view_to_cart, rec_cart_to_purchase, rec_overall],
        improvements
    )):
        fig.add_annotation(
            x=x, y=y + 3,
            text=f"+{imp:.1f}%",
            showarrow=False,
            font=dict(color=COLORS['positive'])
        )
    
    # Update layout
    fig.update_layout(
        title="Conversion Rate Comparison",
        xaxis_title="Conversion Stage",
        yaxis_title="Conversion Rate (%)",
        plot_bgcolor=COLORS['background'],
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color=COLORS['primary']),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        margin=dict(l=40, r=40, t=60, b=40),
    )
    
    return fig

def create_return_rate_chart(df):
    """Create return rate chart comparing control vs recommendation groups"""
    # Calculate return rates by category
    categories = df['product_category'].unique()
    
    control_returns = []
    rec_returns = []
    
    for category in categories:
        cat_df = df[df['product_category'] == category]
        
        control_cat_df = cat_df[(cat_df['test_group'] == 'Control') & (cat_df['purchased'] == 1)]
        rec_cat_df = cat_df[(cat_df['test_group'] == 'Size Recommendation') & (cat_df['purchased'] == 1)]
        
        control_return_rate = control_cat_df['returned'].mean() * 100 if len(control_cat_df) > 0 else 0
        rec_return_rate = rec_cat_df['returned'].mean() * 100 if len(rec_cat_df) > 0 else 0
        
        control_returns.append(control_return_rate)
        rec_returns.append(rec_return_rate)
    
    # Create the figure
    fig = go.Figure()
    
    # Add lines
    fig.add_trace(go.Scatter(
        x=categories,
        y=control_returns,
        mode='lines+markers',
        name='Control',
        line=dict(color=COLORS['secondary'], width=3),
        marker=dict(size=10, color=COLORS['secondary'])
    ))
    
    fig.add_trace(go.Scatter(
        x=categories,
        y=rec_returns,
        mode='lines+markers',
        name='Size Recommendation',
        line=dict(color=COLORS['primary'], width=3),
        marker=dict(size=10, color=COLORS['primary'])
    ))
    
    # Add improvement annotations
    for i, (cat, ctrl, rec) in enumerate(zip(categories, control_returns, rec_returns)):
        reduction = ((ctrl - rec) / ctrl * 100) if ctrl > 0 else 0
        fig.add_annotation(
            x=cat, y=rec - 2,
            text=f"-{reduction:.1f}%",
            showarrow=False,
            font=dict(color=COLORS['positive'])
        )
    
    # Update layout
    fig.update_layout(
        title="Return Rate by Product Category",
        xaxis_title="Product Category",
        yaxis_title="Return Rate (%)",
        plot_bgcolor=COLORS['background'],
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color=COLORS['primary']),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        margin=dict(l=40, r=40, t=60, b=40),
    )
    
    return fig

def create_satisfaction_chart(df):
    """Create customer satisfaction chart comparing control vs recommendation groups"""
    # Filter only purchased items with satisfaction scores
    purchased_df = df[df['purchased'] == 1]
    
    # Group by test group and calculate average satisfaction
    satisfaction_by_group = purchased_df.groupby('test_group')['satisfaction_score'].mean().reset_index()
    
    # Create the figure
    fig = go.Figure()
    
    # Add bars
    fig.add_trace(go.Bar(
        x=satisfaction_by_group['test_group'],
        y=satisfaction_by_group['satisfaction_score'],
        marker_color=[COLORS['secondary'], COLORS['primary']],
        text=satisfaction_by_group['satisfaction_score'].round(1),
        textposition='auto',
    ))
    
    # Calculate improvement
    control_score = satisfaction_by_group[satisfaction_by_group['test_group'] == 'Control']['satisfaction_score'].values[0]
    rec_score = satisfaction_by_group[satisfaction_by_group['test_group'] == 'Size Recommendation']['satisfaction_score'].values[0]
    improvement = ((rec_score - control_score) / control_score) * 100
    
    # Add improvement annotation
    fig.add_annotation(
        x='Size Recommendation',
        y=rec_score + 0.3,
        text=f"+{improvement:.1f}%",
        showarrow=False,
        font=dict(color=COLORS['positive'])
    )
    
    # Update layout
    fig.update_layout(
        title="Average Customer Satisfaction Score (1-10)",
        xaxis_title="Test Group",
        yaxis_title="Satisfaction Score",
        plot_bgcolor=COLORS['background'],
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color=COLORS['primary']),
        margin=dict(l=40, r=40, t=60, b=40),
    )
    
    return fig

def create_roi_chart(investment_amount, conversion_increase, aov, monthly_visitors):
    """Create ROI projection chart based on input parameters"""
    # Calculate monthly additional revenue
    monthly_additional_revenue = monthly_visitors * (conversion_increase / 100) * aov
    
    # Calculate ROI over 24 months
    months = list(range(1, 25))
    cumulative_revenue = [monthly_additional_revenue * month for month in months]
    roi_percentage = [(revenue - investment_amount) / investment_amount * 100 for revenue in cumulative_revenue]
    
    # Create the figure
    fig = go.Figure()
    
    # Add breakeven line
    breakeven_month = next((i for i, rev in enumerate(cumulative_revenue) if rev >= investment_amount), None)
    if breakeven_month is not None:
        fig.add_vline(
            x=breakeven_month + 1, 
            line_dash="dash", 
            line_color=COLORS['positive'],
            annotation_text=f"Breakeven at month {breakeven_month + 1}",
            annotation_position="top right"
        )
    
    # Add revenue line
    fig.add_trace(go.Scatter(
        x=months,
        y=cumulative_revenue,
        mode='lines',
        name='Cumulative Revenue',
        line=dict(color=COLORS['primary'], width=3)
    ))
    
    # Add investment line
    fig.add_trace(go.Scatter(
        x=months,
        y=[investment_amount] * len(months),
        mode='lines',
        name='Investment Amount',
        line=dict(color=COLORS['secondary'], width=2, dash='dash')
    ))
    
    # Update layout
    fig.update_layout(
        title="ROI Projection Over 24 Months",
        xaxis_title="Month",
        yaxis_title="Amount ($)",
        plot_bgcolor=COLORS['background'],
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color=COLORS['primary']),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        margin=dict(l=40, r=40, t=60, b=40),
    )
    
    return fig