import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

from src.data_processing import load_data, filter_data
from src.metrics.conversion_rates import calculate_conversion_by_category
from src.metrics.return_rates import calculate_return_by_category
from src.metrics.satisfaction import calculate_satisfaction_by_category

# Color palette for consistent styling
COLORS = {
    'primary': '#d0d0d0',    # Light gray
    'secondary': '#808080',  # Medium gray
    'accent': '#ffffff',     # White
    'background': '#101010', # Near black
    'positive': '#a0e4b0',   # Muted green
    'negative': '#e4a0a0'    # Muted red
}

def SegmentExplorer():
    """Segment Explorer component for analyzing data across different product categories"""
    st.title("Segment Explorer")
    st.markdown("### Analyze performance across different product categories")
    
    # Load data
    data = load_data()
    
    # Date range filter
    st.sidebar.markdown("### Time Period")
    
    min_date = pd.to_datetime(data['date']).min().date()
    max_date = pd.to_datetime(data['date']).max().date()
    
    date_range = st.sidebar.date_input(
        "Date Range",
        value=[min_date, max_date],
        min_value=min_date,
        max_value=max_date
    )
    
    # Apply date filter
    if len(date_range) == 2:
        filtered_data = filter_data(data, date_range=date_range)
    else:
        filtered_data = data.copy()
    
    # Calculate metrics by category
    conversion_by_category = calculate_conversion_by_category(filtered_data)
    return_by_category = calculate_return_by_category(filtered_data)
    satisfaction_by_category = calculate_satisfaction_by_category(filtered_data)
    
    # Metric selection
    st.markdown("## Choose Metrics to Explore")
    
    metric_options = [
        "Conversion Rate Improvement",
        "Return Rate Reduction",
        "Satisfaction Score Improvement"
    ]
    
    selected_metrics = st.multiselect(
        "Select metrics to visualize",
        options=metric_options,
        default=["Conversion Rate Improvement", "Return Rate Reduction"]
    )
    
    # Display selected metric visualizations
    st.markdown("## Category Performance")
    
    if "Conversion Rate Improvement" in selected_metrics:
        # Create conversion rate comparison chart
        fig = go.Figure()
        
        categories = conversion_by_category['category']
        
        # Add bars for control group
        fig.add_trace(go.Bar(
            x=categories,
            y=conversion_by_category['control_conversion'],
            name='Without Size Recommendation',
            marker_color=COLORS['secondary']
        ))
        
        # Add bars for recommendation group
        fig.add_trace(go.Bar(
            x=categories,
            y=conversion_by_category['recommendation_conversion'],
            name='With Size Recommendation',
            marker_color=COLORS['primary']
        ))
        
        # Add improvement annotations
        for i, category in enumerate(categories):
            control = conversion_by_category['control_conversion'].iloc[i]
            recommendation = conversion_by_category['recommendation_conversion'].iloc[i]
            improvement = conversion_by_category['improvement'].iloc[i]
            
            fig.add_annotation(
                x=category,
                y=recommendation + 0.5,
                text=f"+{improvement:.1f}%",
                showarrow=False,
                font=dict(color=COLORS['positive'])
            )
        
        # Update layout
        fig.update_layout(
            title="Conversion Rate by Product Category",
            xaxis_title="Product Category",
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
        
        st.plotly_chart(fig, use_container_width=True)
    
    if "Return Rate Reduction" in selected_metrics:
        # Create return rate comparison chart
        fig = go.Figure()
        
        categories = return_by_category['category']
        
        # Add bars for control group
        fig.add_trace(go.Bar(
            x=categories,
            y=return_by_category['control_return_rate'],
            name='Without Size Recommendation',
            marker_color=COLORS['secondary']
        ))
        
        # Add bars for recommendation group
        fig.add_trace(go.Bar(
            x=categories,
            y=return_by_category['recommendation_return_rate'],
            name='With Size Recommendation',
            marker_color=COLORS['primary']
        ))
        
        # Add reduction annotations
        for i, category in enumerate(categories):
            control = return_by_category['control_return_rate'].iloc[i]
            recommendation = return_by_category['recommendation_return_rate'].iloc[i]
            reduction = return_by_category['reduction'].iloc[i]
            
            fig.add_annotation(
                x=category,
                y=recommendation + 0.5,
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
        
        st.plotly_chart(fig, use_container_width=True)
    
    if "Satisfaction Score Improvement" in selected_metrics:
        # Create satisfaction score comparison chart
        fig = go.Figure()
        
        categories = satisfaction_by_category['category']
        
        # Add bars for control group
        fig.add_trace(go.Bar(
            x=categories,
            y=satisfaction_by_category['control_satisfaction'],
            name='Without Size Recommendation',
            marker_color=COLORS['secondary']
        ))
        
        # Add bars for recommendation group
        fig.add_trace(go.Bar(
            x=categories,
            y=satisfaction_by_category['recommendation_satisfaction'],
            name='With Size Recommendation',
            marker_color=COLORS['primary']
        ))
        
        # Add improvement annotations
        for i, category in enumerate(categories):
            control = satisfaction_by_category['control_satisfaction'].iloc[i]
            recommendation = satisfaction_by_category['recommendation_satisfaction'].iloc[i]
            improvement = satisfaction_by_category['improvement'].iloc[i]
            
            fig.add_annotation(
                x=category,
                y=recommendation + 0.2,
                text=f"+{improvement:.1f}%",
                showarrow=False,
                font=dict(color=COLORS['positive'])
            )
        
        # Update layout
        fig.update_layout(
            title="Satisfaction Score by Product Category",
            xaxis_title="Product Category",
            yaxis_title="Satisfaction Score (1-10)",
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
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Category comparison table
    st.markdown("## Category Comparison Table")
    
    # Merge all category data
    merged_data = conversion_by_category.merge(
        return_by_category, on='category'
    ).merge(
        satisfaction_by_category, on='category'
    )
    
    # Select columns to display
    display_data = merged_data[['category', 
                               'improvement', 
                               'reduction', 
                               'improvement_y']].copy()
    
    # Rename columns
    display_data.columns = [
        'Product Category', 
        'Conversion Rate Improvement (%)', 
        'Return Rate Reduction (%)', 
        'Satisfaction Improvement (%)'
    ]
    
    # Format numbers
    for col in display_data.columns[1:]:
        display_data[col] = display_data[col].round(1)
    
    # Sort by conversion improvement
    display_data = display_data.sort_values('Conversion Rate Improvement (%)', ascending=False)
    
    # Display table
    st.dataframe(display_data, use_container_width=True)
    
    # Insights section
    st.markdown("## Category Insights")
    
    # Find best and worst performing categories
    best_conversion_category = display_data.iloc[0]['Product Category']
    best_conversion_improvement = display_data.iloc[0]['Conversion Rate Improvement (%)']
    
    best_return_idx = display_data['Return Rate Reduction (%)'].idxmax()
    best_return_category = display_data.loc[best_return_idx]['Product Category']
    best_return_reduction = display_data.loc[best_return_idx]['Return Rate Reduction (%)']
    
    worst_conversion_idx = display_data['Conversion Rate Improvement (%)'].idxmin()
    worst_conversion_category = display_data.loc[worst_conversion_idx]['Product Category']
    worst_conversion_improvement = display_data.loc[worst_conversion_idx]['Conversion Rate Improvement (%)']
    
    # Display insights
    st.markdown(
        f"""
        ### Key Findings:
        
        - **{best_conversion_category}** shows the strongest conversion improvement (+{best_conversion_improvement}%), 
          suggesting size recommendations are particularly effective for this category.
          
        - **{best_return_category}** has the largest return rate reduction (-{best_return_reduction}%), 
          indicating that accurate sizing is especially important for this category.
          
        - **{worst_conversion_category}** shows the smallest conversion improvement (+{worst_conversion_improvement}%), 
          which may indicate different sizing challenges or that customers in this category have different purchasing behaviors.
        
        ### Recommendations:
        
        - Focus marketing efforts for size recommendation technology on **{best_conversion_category}** and **{best_return_category}** 
          categories for maximum impact.
          
        - Consider enhanced size recommendation algorithms for **{worst_conversion_category}** to improve effectiveness.
          
        - Use category-specific insights to tailor size recommendation implementations for different product types.
        """
    )