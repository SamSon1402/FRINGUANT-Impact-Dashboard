import streamlit as st
import pandas as pd
import numpy as np

from src.data_processing import load_data
from src.visualization import create_roi_chart
from src.metrics.conversion_rates import calculate_conversion_metrics
from src.metrics.return_rates import calculate_return_metrics

def ROICalculator():
    """ROI Calculator component"""
    st.title("ROI Calculator")
    st.markdown("### Estimate the financial impact of size recommendations")
    
    # Load data to get default values
    data = load_data()
    conversion_metrics = calculate_conversion_metrics(data)
    return_metrics = calculate_return_metrics(data)
    
    # Get default improvement values
    default_conversion_increase = conversion_metrics['overall']['improvement']
    default_return_reduction = return_metrics['overall']['reduction']
    
    # Create input form
    st.markdown("## Business Parameters")
    
    col1, col2 = st.columns(2)
    
    with col1:
        monthly_visitors = st.number_input(
            "Monthly Website Visitors",
            min_value=1000,
            max_value=10000000,
            value=100000,
            step=10000
        )
        
        current_conversion = st.slider(
            "Current Conversion Rate (%)",
            min_value=0.1,
            max_value=10.0,
            value=2.5,
            step=0.1
        )
        
        aov = st.number_input(
            "Average Order Value ($)",
            min_value=10,
            max_value=1000,
            value=85,
            step=5
        )
    
    with col2:
        current_return_rate = st.slider(
            "Current Return Rate (%)",
            min_value=1.0,
            max_value=50.0,
            value=20.0,
            step=0.5
        )
        
        return_processing_cost = st.number_input(
            "Average Return Processing Cost ($)",
            min_value=5,
            max_value=100,
            value=15,
            step=1
        )
        
        implementation_cost = st.number_input(
            "Size Recommendation Implementation Cost ($)",
            min_value=5000,
            max_value=200000,
            value=25000,
            step=1000
        )
    
    # Improvement parameters
    st.markdown("## Expected Improvements")
    st.markdown("Based on our A/B testing data, you can adjust expected improvement percentages:")
    
    col1, col2 = st.columns(2)
    
    with col1:
        conversion_increase = st.slider(
            "Conversion Rate Increase (%)",
            min_value=1.0,
            max_value=50.0,
            value=float(default_conversion_increase),
            step=0.5
        )
    
    with col2:
        return_reduction = st.slider(
            "Return Rate Reduction (%)",
            min_value=1.0,
            max_value=50.0,
            value=float(default_return_reduction),
            step=0.5
        )
    
    # Calculate ROI metrics
    st.markdown("## ROI Analysis")
    
    # Before implementation
    monthly_orders_before = monthly_visitors * (current_conversion / 100)
    monthly_revenue_before = monthly_orders_before * aov
    monthly_returns_before = monthly_orders_before * (current_return_rate / 100)
    monthly_return_cost_before = monthly_returns_before * return_processing_cost
    
    # After implementation
    new_conversion_rate = current_conversion * (1 + conversion_increase / 100)
    new_return_rate = current_return_rate * (1 - return_reduction / 100)
    
    monthly_orders_after = monthly_visitors * (new_conversion_rate / 100)
    monthly_revenue_after = monthly_orders_after * aov
    monthly_returns_after = monthly_orders_after * (new_return_rate / 100)
    monthly_return_cost_after = monthly_returns_after * return_processing_cost
    
    # Calculate impact
    additional_monthly_revenue = monthly_revenue_after - monthly_revenue_before
    monthly_return_cost_savings = monthly_return_cost_before - monthly_return_cost_after
    total_monthly_benefit = additional_monthly_revenue + monthly_return_cost_savings
    
    # ROI calculation
    months_to_breakeven = implementation_cost / total_monthly_benefit if total_monthly_benefit > 0 else float('inf')
    one_year_roi = (total_monthly_benefit * 12 - implementation_cost) / implementation_cost * 100 if implementation_cost > 0 else float('inf')
    
    # Display metrics
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(
            f"""
            <div class="data-card">
                <h3>Monthly Impact</h3>
                <p>Additional Revenue: <span class="positive-change">${additional_monthly_revenue:.2f}</span></p>
                <p>Return Cost Savings: <span class="positive-change">${monthly_return_cost_savings:.2f}</span></p>
                <p>Total Monthly Benefit: <span class="positive-change">${total_monthly_benefit:.2f}</span></p>
            </div>
            """, 
            unsafe_allow_html=True
        )
    
    with col2:
        st.markdown(
            f"""
            <div class="data-card">
                <h3>Return on Investment</h3>
                <p>Implementation Cost: ${implementation_cost:.2f}</p>
                <p>Months to Breakeven: {months_to_breakeven:.1f}</p>
                <p>1-Year ROI: <span class="positive-change">{one_year_roi:.1f}%</span></p>
            </div>
            """, 
            unsafe_allow_html=True
        )
    
    # ROI Chart
    st.plotly_chart(create_roi_chart(implementation_cost, conversion_increase, aov, monthly_visitors), use_container_width=True)
    
    # Summary
    st.markdown("## Summary")
    
    if months_to_breakeven <= 12:
        roi_assessment = f"The investment pays for itself in {months_to_breakeven:.1f} months with a strong 1-year ROI of {one_year_roi:.1f}%."
    else:
        roi_assessment = f"The investment has a longer payback period of {months_to_breakeven:.1f} months, but still provides value through improved customer experience."
    
    st.markdown(
        f"""
        Based on your inputs, implementing FRINGUANT's size recommendation technology would generate:
        
        - ${additional_monthly_revenue:.2f} in additional monthly revenue through improved conversion
        - ${monthly_return_cost_savings:.2f} in monthly savings from reduced returns
        - ${total_monthly_benefit * 12:.2f} total annual benefit
        
        {roi_assessment}
        """
    )