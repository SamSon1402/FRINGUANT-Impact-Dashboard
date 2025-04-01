import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

from src.data_processing import load_data, filter_data
from src.visualization import (
    create_conversion_chart, 
    create_return_rate_chart, 
    create_satisfaction_chart
)
from src.metrics.conversion_rates import calculate_conversion_metrics
from src.metrics.return_rates import calculate_return_metrics, calculate_return_cost_savings
from src.metrics.satisfaction import calculate_satisfaction_metrics
from src.metrics.ab_testing import (
    perform_conversion_ab_test, 
    perform_return_rate_ab_test, 
    perform_satisfaction_ab_test
)

def Dashboard():
    """Main dashboard component"""
    st.title("FRINGUANT Size Recommendation Impact")
    st.markdown("### E-commerce Performance Dashboard")
    
    # Load data
    data = load_data()
    
    # Sidebar filters
    st.sidebar.markdown("### Filters")
    
    # Category filter
    categories = ['All Categories'] + list(data['product_category'].unique())
    selected_category = st.sidebar.selectbox("Product Category", categories)
    
    # Date range filter
    min_date = pd.to_datetime(data['date']).min().date()
    max_date = pd.to_datetime(data['date']).max().date()
    
    date_range = st.sidebar.date_input(
        "Date Range",
        value=[min_date, max_date],
        min_value=min_date,
        max_value=max_date
    )
    
    # Apply filters
    if len(date_range) == 2:
        filtered_data = filter_data(data, 
                                   category=selected_category if selected_category != 'All Categories' else None,
                                   date_range=date_range)
    else:
        filtered_data = filter_data(data, 
                                   category=selected_category if selected_category != 'All Categories' else None)
    
    # KPI Cards Row
    st.markdown("## Key Performance Indicators")
    
    # Calculate metrics
    conversion_metrics = calculate_conversion_metrics(filtered_data)
    return_metrics = calculate_return_metrics(filtered_data)
    satisfaction_metrics = calculate_satisfaction_metrics(filtered_data)
    
    # A/B test results
    conversion_ab_test = perform_conversion_ab_test(filtered_data)
    return_ab_test = perform_return_rate_ab_test(filtered_data)
    satisfaction_ab_test = perform_satisfaction_ab_test(filtered_data)
    
    # Return cost savings
    cost_savings = calculate_return_cost_savings(filtered_data)
    
    # Create columns for KPI cards
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(
            f"""
            <div class="data-card">
                <h3>Conversion Rate</h3>
                <p>With Size Recommendation: {conversion_metrics['overall']['recommendation']:.2f}%</p>
                <p>Without: {conversion_metrics['overall']['control']:.2f}%</p>
                <p class="positive-change">+{conversion_metrics['overall']['improvement']:.2f}% Increase</p>
                <p>Confidence: {conversion_ab_test['confidence']:.1f}%</p>
            </div>
            """, 
            unsafe_allow_html=True
        )
    
    with col2:
        st.markdown(
            f"""
            <div class="data-card">
                <h3>Return Rate</h3>
                <p>With Size Recommendation: {return_metrics['overall']['recommendation']:.2f}%</p>
                <p>Without: {return_metrics['overall']['control']:.2f}%</p>
                <p class="positive-change">-{return_metrics['overall']['reduction']:.2f}% Reduction</p>
                <p>Confidence: {return_ab_test['confidence']:.1f}%</p>
            </div>
            """, 
            unsafe_allow_html=True
        )
    
    with col3:
        st.markdown(
            f"""
            <div class="data-card">
                <h3>Customer Satisfaction</h3>
                <p>With Size Recommendation: {satisfaction_metrics['overall']['recommendation']:.2f}/10</p>
                <p>Without: {satisfaction_metrics['overall']['control']:.2f}/10</p>
                <p class="positive-change">+{satisfaction_metrics['overall']['improvement']:.2f}% Improvement</p>
                <p>Confidence: {satisfaction_ab_test['confidence']:.1f}%</p>
            </div>
            """, 
            unsafe_allow_html=True
        )
    
    with col4:
        st.markdown(
            f"""
            <div class="data-card">
                <h3>Return Cost Savings</h3>
                <p>Estimated Savings: ${cost_savings:.2f}</p>
                <p>Based on $15 average return cost</p>
                <p class="positive-change">Projected Annual: ${cost_savings * 12:.2f}</p>
            </div>
            """, 
            unsafe_allow_html=True
        )
    
    # Charts
    st.markdown("## Impact Analysis")
    
    # Conversion Rate Chart
    st.plotly_chart(create_conversion_chart(filtered_data), use_container_width=True)
    
    # Return Rate Chart
    st.plotly_chart(create_return_rate_chart(filtered_data), use_container_width=True)
    
    # Satisfaction Chart
    st.plotly_chart(create_satisfaction_chart(filtered_data), use_container_width=True)
    
    # Summary Section
    st.markdown("## Summary")
    
    st.markdown(
        f"""
        The implementation of FRINGUANT's size recommendation technology has demonstrated significant positive impacts:
        
        - **{conversion_metrics['overall']['improvement']:.1f}%** increase in overall conversion rate
        - **{return_metrics['overall']['reduction']:.1f}%** reduction in product returns
        - **{satisfaction_metrics['overall']['improvement']:.1f}%** improvement in customer satisfaction scores
        - Estimated annual return processing cost savings of **${cost_savings * 12:.2f}**
        
        These improvements directly translate to increased revenue, reduced operational costs, and enhanced customer experience.
        """
    )