"""Streamlit Frontend Application for B H Enterprises."""

import streamlit as st
import requests
import json
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Page configuration
st.set_page_config(
    page_title="B H Enterprises - Building Materials & Home Decorator",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS
st.markdown(
    """
    <style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .service-card {
        background: #f0f2f6;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #667eea;
    }
    .contact-form {
        background: #f8f9fa;
        padding: 2rem;
        border-radius: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# API Configuration - Load from secrets
API_BASE_URL = st.secrets.get("API_URL", "http://localhost:8000")
CONTACT_EMAIL = st.secrets.get("CONTACT_EMAIL", "Jafar@bhenterprises.com")
CONTACT_PHONE = st.secrets.get("CONTACT_PHONE", "+91-8882302674")
GEMINI_API_KEY = st.secrets.get("GEMINI_API_KEY", "")


def fetch_from_api(endpoint):
    """Fetch data from API."""
    try:
        response = requests.get(f"{API_BASE_URL}{endpoint}", timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"API Error: {e}")
        st.error(f"Unable to fetch data: {str(e)}")
        return None


def post_to_api(endpoint, data):
    """Post data to API."""
    try:
        response = requests.post(f"{API_BASE_URL}{endpoint}", json=data, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"API Error: {e}")
        st.error(f"Unable to submit form: {str(e)}")
        return None


# Main Header
st.markdown(
    """
    <div class="main-header">
        <h1>🏠 B H Enterprises</h1>
        <p>Premium Building Materials & Professional Home Decorator Services</p>
        <p>GST: 07ETTPM3697B1Z4 | Bangalore, India</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# Navigation
page = st.sidebar.radio(
    "Navigation",
    ["Home", "About Us", "Services", "Contact", "Get Quote", "FAQ", "Testimonials"],
)

# ==================== HOME ====================
if page == "Home":
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ## Welcome to B H Enterprises
        
        We are your trusted partner for:
        - **Premium Building Materials**
        - **Professional Home Decoration**
        - **Quality Assurance**
        - **Timely Project Delivery**
        
        With years of experience, we deliver excellence in every project.
        """)
    
    with col2:
        st.image("https://via.placeholder.com/400x300?text=B+H+Enterprises", 
                caption="Quality Home Solutions")
    
    st.divider()
    
    # Key Stats
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Customer Rating", "4.8/5", "+0.2")
    with col2:
        st.metric("Projects Completed", "500+", "")
    with col3:
        st.metric("Happy Customers", "1000+", "")


# ==================== ABOUT ====================
elif page == "About Us":
    about_data = fetch_from_api("/api/contact/about")
    
    if about_data:
        st.markdown(f"## {about_data['company_name']}")
        st.write(about_data['description'])
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### Our Services")
            for service in about_data.get('services', []):
                st.write(f"✓ {service}")
        
        with col2:
            st.markdown("### Why Choose Us")
            for reason in about_data.get('why_choose_us', []):
                st.write(f"✓ {reason}")


# ==================== SERVICES ====================
elif page == "Services":
    st.markdown("## Our Services")
    
    services = [
        {
            "name": "White Cement Supply",
            "description": "Premium quality white cement for finest finishing",
            "icon": "🏗️"
        },
        {
            "name": "Professional Painting",
            "description": "Interior and exterior painting with premium paints",
            "icon": "🎨"
        },
        {
            "name": "Carpenter Work",
            "description": "Custom carpentry and woodwork solutions",
            "icon": "🪵"
        },
        {
            "name": "Tile Installation",
            "description": "Expert tile fixing and installation services",
            "icon": "🟦"
        },
    ]
    
    cols = st.columns(2)
    for idx, service in enumerate(services):
        with cols[idx % 2]:
            st.markdown(
                f"""
                <div class="service-card">
                    <h4>{service['icon']} {service['name']}</h4>
                    <p>{service['description']}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )


# ==================== CONTACT ====================
elif page == "Contact":
    st.markdown("## Get in Touch")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Contact Information")
        st.write(f"📞 {CONTACT_PHONE}")
        st.write(f"📧 {CONTACT_EMAIL}")
        st.write("📍 Bangalore, India")
        st.write("🏢 GST: 07ETTPM3697B1Z4")
    
    with col2:
        st.markdown("### Business Hours")
        st.write("Monday - Friday: 9:00 AM - 6:00 PM")
        st.write("Saturday: 10:00 AM - 4:00 PM")
        st.write("Sunday: Closed")
    
    st.divider()
    
    st.markdown("### Contact Form")
    with st.form("contact_form"):
        name = st.text_input("Full Name *", placeholder="Your name")
        email = st.text_input("Email Address *", placeholder="your.email@example.com")
        phone = st.text_input("Phone Number *", placeholder="+91-XXXXXXXXXX")
        subject = st.text_input("Subject *", placeholder="How can we help?")
        category = st.selectbox("Category", ["General", "Products", "Services"])
        message = st.text_area("Message *", placeholder="Your message here...", height=150)
        
        submit_button = st.form_submit_button("Send Message", use_container_width=True)
        
        if submit_button:
            if not all([name, email, phone, subject, message]):
                st.error("Please fill all required fields")
            else:
                contact_data = {
                    "name": name,
                    "email": email,
                    "phone": phone,
                    "subject": subject,
                    "message": message,
                    "category": category.lower(),
                }
                
                result = post_to_api("/api/contact/submit", contact_data)
                if result:
                    st.success("✅ Thank you! Your message has been sent successfully.")
                    st.balloons()


# ==================== GET QUOTE ====================
elif page == "Get Quote":
    st.markdown("## Request a Custom Quote")
    
    with st.form("quote_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("Full Name *", placeholder="Your name")
            email = st.text_input("Email *", placeholder="your.email@example.com")
            phone = st.text_input("Phone *", placeholder="+91-XXXXXXXXXX")
        
        with col2:
            project_type = st.selectbox("Project Type *", [
                "Interior Painting",
                "Carpenter Work",
                "Tile Installation",
                "Complete Home Decoration",
                "Other"
            ])
            budget_range = st.selectbox("Budget Range", [
                "Below ₹50,000",
                "₹50,000 - ₹1,00,000",
                "₹1,00,000 - ₹5,00,000",
                "Above ₹5,00,000",
                "Not Sure"
            ])
            area_sq_ft = st.number_input("Area (Sq. Ft.)", min_value=0.0, step=100.0)
        
        description = st.text_area("Project Description *", 
                                  placeholder="Tell us about your project...", 
                                  height=150)
        
        submit_quote = st.form_submit_button("Request Quote", use_container_width=True)
        
        if submit_quote:
            if not all([name, email, phone, project_type, description]):
                st.error("Please fill all required fields")
            else:
                quote_data = {
                    "name": name,
                    "email": email,
                    "phone": phone,
                    "project_type": project_type,
                    "description": description,
                    "budget_range": budget_range,
                    "area_sq_ft": area_sq_ft if area_sq_ft > 0 else None,
                }
                
                result = post_to_api("/api/contact/quote-request", quote_data)
                if result:
                    st.success("✅ Quote request submitted! We'll contact you soon.")
                    st.balloons()


# ==================== FAQ ====================
elif page == "FAQ":
    st.markdown("## Frequently Asked Questions")
    
    faq_data = fetch_from_api("/api/contact/faq")
    
    if faq_data:
        for faq in faq_data.get('faqs', []):
            with st.expander(f"❓ {faq['question']}"):
                st.write(faq['answer'])


# ==================== TESTIMONIALS ====================
elif page == "Testimonials":
    st.markdown("## Customer Testimonials")
    
    testimonials_data = fetch_from_api("/api/contact/testimonials")
    
    if testimonials_data:
        col1, col2, col3 = st.columns(3)
        
        avg_rating = testimonials_data.get('average_rating', 0)
        col1.metric("Average Rating", f"{avg_rating}/5.0", "⭐")
        col2.metric("Total Reviews", testimonials_data.get('total', 0))
        col3.metric("Satisfaction Rate", "98%", "✅")
        
        st.divider()
        
        for testimonial in testimonials_data.get('testimonials', []):
            col1, col2 = st.columns([0.15, 0.85])
            
            with col1:
                st.write("⭐" * int(testimonial['rating']))
            
            with col2:
                st.markdown(f"### {testimonial['customer_name']}")
                st.write(f"**Project:** {testimonial['project']}")
                st.write(f"*{testimonial['feedback']}*")
            
            st.divider()


# ==================== SIDEBAR INFO ====================
st.sidebar.divider()
st.sidebar.markdown("### About")
st.sidebar.info(
    f"""
    **B H Enterprises**
    
    Premium Building Materials & Home Decorator Services
    
    📞 {CONTACT_PHONE}
    📧 {CONTACT_EMAIL}
    🏢 Bangalore, India
    """
)

st.sidebar.markdown("### Links")
st.sidebar.link_button("🌐 Visit Website", "https://bhenterprises.com")
st.sidebar.link_button("📘 Facebook", "https://www.facebook.com/bhenterprises")
st.sidebar.link_button("📸 Instagram", "https://www.instagram.com/bhenterprises")

st.sidebar.markdown("---")
st.sidebar.caption("© 2024 B H Enterprises. All rights reserved.")
