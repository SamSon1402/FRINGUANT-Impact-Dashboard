import streamlit as st
from pathlib import Path
import pandas as pd
import numpy as np
import base64
from datetime import datetime, timedelta
import plotly.graph_objects as go
from PIL import Image
import time

# Import components
from src.components.dashboard import Dashboard
from src.components.roi_calculator import ROICalculator
from src.components.segment_explorer import SegmentExplorer
from src.components.sustainability_tracker import SustainabilityTracker
from src.components.selfie_accuracy import SelfieAccuracyAnalyzer
from src.components.customer_journey import CustomerJourney
from src.components.ab_testing import ABTestingPanel
from src.components.predictive_analytics import PredictiveAnalytics
from src.components.demographics import DemographicInsights
from src.components.brand_timeline import BrandTimeline

# Set page configuration
st.set_page_config(
    page_title="FRINGUANT Impact Dashboard",
    page_icon="📏",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load custom CSS
def load_css():
    css_file = Path("assets/styles/style.css")
    with open(css_file) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def add_bg_from_local(image_file):
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()
    
    bg_img = f"""
    <style>
    .stApp {{
        background-image: url("data:image/jpg;base64,{encoded_string}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}
    </style>
    """
    st.markdown(bg_img, unsafe_allow_html=True)

# Add loading animation
def show_loading_animation():
    st.markdown(
        """
        <div class="loading-container">
            <div class="loading-spinner"></div>
            <p class="loading-text">Loading dashboard data...</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    time.sleep(1)  # Simulate loading

# Add animated elements
def add_animated_elements():
    st.markdown(
        """
        <div class="animated-background">
            <div class="gradient-orb orb1"></div>
            <div class="gradient-orb orb2"></div>
            <div class="gradient-orb orb3"></div>
            <div class="mesh-grid"></div>
        </div>
        """,
        unsafe_allow_html=True
    )

# Add animated notification
def add_notification():
    st.markdown(
        """
        <div class="notification-toast">
            <div class="notification-icon">🔔</div>
            <div class="notification-content">
                <p class="notification-title">New Data Available</p>
                <p class="notification-message">Latest metrics have been updated</p>
            </div>
            <div class="notification-close">×</div>
        </div>
        """,
        unsafe_allow_html=True
    )

# Load background image
add_bg_from_local("assets/images/background.jpg")
load_css()
add_animated_elements()

# Show loading animation
show_loading_animation()

# Add notification
add_notification()

# Sidebar with animated logo and navigation
with st.sidebar:
    st.markdown(
        """
        <div class="logo-container">
            <img src="data:image/png;base64,YOUR_LOGO_BASE64" class="logo-image">
            <div class="logo-text">FRINGUANT</div>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    st.markdown("<p class='tagline'>Size Perfect. Every Time.</p>", unsafe_allow_html=True)
    
    st.markdown("<div class='sidebar-divider'></div>", unsafe_allow_html=True)
    
    # Animated navigation menu
    st.markdown("<div class='nav-header'>DASHBOARD MODULES</div>", unsafe_allow_html=True)
    
    # Create stylized navigation menu
    menu_options = [
        "📊 Performance Overview",
        "💰 ROI Calculator",
        "🔍 Segment Explorer",
        "🌿 Sustainability Impact",
        "📷 Selfie Accuracy",
        "🛒 Customer Journey",
        "🧪 A/B Testing Lab",
        "📈 Predictive Analytics",
        "👥 Demographic Insights",
        "🚀 Brand Growth Timeline"
    ]
    
    # Custom navigation with animations
    for i, option in enumerate(menu_options):
        if st.sidebar.button(option, key=f"nav_{i}", help=f"Navigate to {option}"):
            nav = option
            st.session_state.nav = option
    
    if 'nav' not in st.session_state:
        st.session_state.nav = menu_options[0]
    
    nav = st.session_state.nav
    
    # Animated timeline progress indicator
    st.markdown("<div class='sidebar-divider'></div>", unsafe_allow_html=True)
    st.markdown("<div class='nav-header'>PROJECT TIMELINE</div>", unsafe_allow_html=True)
    
    st.markdown(
        """
        <div class="timeline-container">
            <div class="timeline-track">
                <div class="timeline-progress" style="width: 65%;"></div>
                <div class="timeline-marker active" style="left: 0%;">
                    <div class="timeline-tooltip">Launch</div>
                </div>
                <div class="timeline-marker active" style="left: 25%;">
                    <div class="timeline-tooltip">50 Brands</div>
                </div>
                <div class="timeline-marker active" style="left: 65%;">
                    <div class="timeline-tooltip">Now</div>
                </div>
                <div class="timeline-marker" style="left: 100%;">
                    <div class="timeline-tooltip">Market Leader</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Date range filter that applies to all pages
    st.markdown("<div class='sidebar-divider'></div>", unsafe_allow_html=True)
    st.markdown("<div class='nav-header'>GLOBAL FILTERS</div>", unsafe_allow_html=True)
    
    # Get date range from simulated data
    from src.data_processing import load_data
    data = load_data()
    min_date = pd.to_datetime(data['date']).min().date()
    max_date = pd.to_datetime(data['date']).max().date()
    
    date_range = st.date_input(
        "Date Range",
        value=[min_date, max_date],
        min_value=min_date,
        max_value=max_date
    )
    
    # Add quick date selectors with animation
    st.markdown(
        """
        <div class="quick-filters">
            <button class="quick-filter-btn" onclick="handleQuickFilter('30d')">
                <span class="quick-filter-icon">📅</span>
                <span class="quick-filter-text">Last 30 Days</span>
            </button>
            <button class="quick-filter-btn" onclick="handleQuickFilter('90d')">
                <span class="quick-filter-icon">📊</span>
                <span class="quick-filter-text">Last Quarter</span>
            </button>
        </div>
        <script>
            function handleQuickFilter(period) {
                // This would be handled by Streamlit
                console.log('Filter: ' + period);
            }
        </script>
        """,
        unsafe_allow_html=True
    )
    
    # Global category filter with animation
    categories = ['All Categories'] + list(data['product_category'].unique())
    selected_category = st.selectbox("Product Category", categories)
    
    # Animated stats in sidebar
    st.markdown("<div class='sidebar-divider'></div>", unsafe_allow_html=True)
    st.markdown("<div class='nav-header'>LIVE METRICS</div>", unsafe_allow_html=True)
    
    st.markdown(
        """
        <div class="sidebar-stats">
            <div class="stat-card">
                <div class="stat-icon">👗</div>
                <div class="stat-value counter">47</div>
                <div class="stat-label">Active Brands</div>
                <div class="stat-trend positive">+3</div>
            </div>
            
            <div class="stat-card">
                <div class="stat-icon">👤</div>
                <div class="stat-value counter">215K</div>
                <div class="stat-label">Active Users</div>
                <div class="stat-trend positive">+12.4%</div>
            </div>
            
            <div class="stat-card">
                <div class="stat-icon">🔄</div>
                <div class="stat-value counter">-68%</div>
                <div class="stat-label">Return Rate</div>
                <div class="stat-trend positive">Improvement</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Footer with animated pulse
    st.markdown("<div class='sidebar-divider'></div>", unsafe_allow_html=True)
    st.markdown(
        f"""
        <div class="sidebar-footer">
            <div class="footer-logo">F</div>
            <div class="footer-text">
                <p>© 2025 FRINGUANT | v2.5.0</p>
                <p class="update-pulse">Last updated: {datetime.now().strftime('%H:%M:%S')}</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

# Apply filters to data for all pages
if len(date_range) == 2:
    filtered_data = data.copy()  # This would actually use the filter_data function
else:
    filtered_data = data.copy()

# Main content area with dynamic header and animations
st.markdown(
    f"""
    <div class="dashboard-header fadeInDown">
        <div class="header-content">
            <div class="header-title-container">
                <h1>{nav.split(' ', 1)[1]}</h1>
                <div class="header-decoration"></div>
            </div>
            <p class="timestamp fadeIn">Data as of {max_date.strftime('%B %d, %Y')}</p>
        </div>
        <div class="header-actions">
            <button class="action-button pulse">
                <span class="action-icon">📊</span>
                <span class="action-text">Export</span>
            </button>
            <button class="action-button">
                <span class="action-icon">🔄</span>
                <span class="action-text">Refresh</span>
            </button>
            <button class="action-button">
                <span class="action-icon">⚙️</span>
                <span class="action-text">Settings</span>
            </button>
        </div>
    </div>
    """, 
    unsafe_allow_html=True
)

# Add module intro animation and description
module_descriptions = {
    "📊 Performance Overview": "Comprehensive analysis of size recommendation impact on key business metrics.",
    "💰 ROI Calculator": "Calculate the financial impact of implementing FRINGUANT's technology.",
    "🔍 Segment Explorer": "Explore performance data across different product categories and customer segments.",
    "🌿 Sustainability Impact": "Track environmental benefits from reduced returns and optimized shipping.",
    "📷 Selfie Accuracy": "Analyze the precision of size predictions from customer selfies.",
    "🛒 Customer Journey": "Visualize the complete customer path and identify optimization opportunities.",
    "🧪 A/B Testing Lab": "Design and monitor experiments to continuously improve recommendations.",
    "📈 Predictive Analytics": "Forecast future performance and identify growth opportunities.",
    "👥 Demographic Insights": "Understand how different customer groups interact with size recommendations.",
    "🚀 Brand Growth Timeline": "Track partner brand onboarding and performance improvements over time."
}

st.markdown(
    f"""
    <div class="module-intro slideInUp">
        <div class="module-icon">{nav.split(' ', 1)[0]}</div>
        <div class="module-description">{module_descriptions[nav]}</div>
    </div>
    """,
    unsafe_allow_html=True
)

# Content based on navigation selection with fade-in animation
st.markdown('<div class="content-container fadeIn">', unsafe_allow_html=True)

if nav == "📊 Performance Overview":
    Dashboard()
    
elif nav == "💰 ROI Calculator":
    ROICalculator()
    
elif nav == "🔍 Segment Explorer":
    SegmentExplorer()
    
elif nav == "🌿 Sustainability Impact":
    SustainabilityTracker()
    
elif nav == "📷 Selfie Accuracy":
    SelfieAccuracyAnalyzer()
    
elif nav == "🛒 Customer Journey":
    CustomerJourney()
    
elif nav == "🧪 A/B Testing Lab":
    ABTestingPanel()
    
elif nav == "📈 Predictive Analytics":
    PredictiveAnalytics()
    
elif nav == "👥 Demographic Insights":
    DemographicInsights()
    
elif nav == "🚀 Brand Growth Timeline":
    BrandTimeline()

st.markdown('</div>', unsafe_allow_html=True)

# Floating action button with animations
st.markdown(
    """
    <div class="floating-action-menu">
        <button class="floating-action-button">
            <span class="fab-icon">+</span>
        </button>
        <div class="floating-action-items">
            <button class="floating-action-item" data-tooltip="Export PDF">
                <span>📄</span>
            </button>
            <button class="floating-action-item" data-tooltip="Share Dashboard">
                <span>📤</span>
            </button>
            <button class="floating-action-item" data-tooltip="Bookmark">
                <span>🔖</span>
            </button>
            <button class="floating-action-item" data-tooltip="Alert Setup">
                <span>⚠️</span>
            </button>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# Add animations for page transitions
st.markdown(
    """
    <script>
        // This would be implemented with actual JavaScript in a real app
        // Simulating animation effects with CSS only for Streamlit
    </script>
    """,
    unsafe_allow_html=True
)