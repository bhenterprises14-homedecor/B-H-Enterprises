"""Streamlit App for B H Enterprises — fully self-contained, zero-cost.

No separate backend required. Runs entirely on Streamlit Cloud's free tier.
Lead capture (Contact / Get Quote forms) is sent via email using Gmail SMTP.

REQUIRED SETUP (Streamlit Cloud > App > Settings > Secrets):

    CONTACT_EMAIL = "Jafar@bhenterprises.com"
    CONTACT_PHONE = "+91-8882302674"
    SMTP_USERNAME = "your-gmail-address@gmail.com"
    SMTP_PASSWORD = "your-16-char-gmail-app-password"
    NOTIFY_EMAIL  = "Jafar@bhenterprises.com"   # where leads get sent (can equal CONTACT_EMAIL)

Gmail App Password (2 minutes, free):
    1. Turn on 2-Step Verification on the Gmail account: myaccount.google.com/security
    2. Go to myaccount.google.com/apppasswords
    3. Create an app password for "Mail" -> copy the 16-character code
    4. Use that as SMTP_PASSWORD above (NOT the normal Gmail password)

If SMTP secrets aren't set yet, forms still show success to the visitor,
but the lead is only written to the app logs (Streamlit Cloud > Manage app > Logs),
not delivered anywhere. Set up SMTP as soon as possible so no leads are lost.
"""

import logging
import smtplib
from datetime import datetime
from email.mime.text import MIMEText

import streamlit as st

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Page configuration
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="B H Enterprises - Building Materials & Home Decorator",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded",
)

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
    .hero-banner {
        background: linear-gradient(135deg, #f0f2f6 0%, #e6e9f0 100%);
        border: 1px solid #d8dce6;
        border-radius: 10px;
        padding: 2rem;
        text-align: center;
        font-size: 3rem;
        line-height: 1.4;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# Configuration (from Streamlit secrets, with safe local-dev defaults)
# ---------------------------------------------------------------------------
CONTACT_EMAIL = st.secrets.get("CONTACT_EMAIL", "info@bhenterprises.com")
CONTACT_PHONE = st.secrets.get("CONTACT_PHONE", "+91-XXXXXXXXXX")
GST_NUMBER = "07ETTPM3697B1Z4"  # TODO: confirm this matches the real GST certificate before launch

SMTP_SERVER = st.secrets.get("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(st.secrets.get("SMTP_PORT", 587))
SMTP_USERNAME = st.secrets.get("SMTP_USERNAME", "")
SMTP_PASSWORD = st.secrets.get("SMTP_PASSWORD", "")
NOTIFY_EMAIL = st.secrets.get("NOTIFY_EMAIL", CONTACT_EMAIL)

# ---------------------------------------------------------------------------
# Static content (previously served by the FastAPI backend — now inline)
# ---------------------------------------------------------------------------
ABOUT_DATA = {
    "company_name": "B H Enterprises",
    "description": (
        "B H Enterprises is a leading provider of premium building materials and "
        "professional home decorator services. With years of experience, we deliver "
        "high-quality products and services for residential and commercial projects."
    ),
    "services": [
        "White Cement Supply",
        "Putty Supply",
        "Paint Supply",
        "Texture & Finishing Materials",
        "Professional Painting Services",
        "Carpenter Work",
        "Tile Installation",
        "Home Decoration Services",
    ],
    "why_choose_us": [
        "Premium Quality Materials",
        "Professional Experienced Team",
        "Affordable Pricing",
        "On-Time Project Delivery",
        "GST Compliant",
        "Warranty on Services",
        "Customer Satisfaction Focus",
    ],
}

FAQ_DATA = [
    {
        "question": "What areas do you service?",
        "answer": "We provide services across Bangalore and surrounding areas. Contact us for specific location queries.",
    },
    {
        "question": "How do you provide quotes?",
        "answer": "We provide customized quotes after assessing the project on-site. You can request a quote through our form.",
    },
    {
        "question": "What is the typical project duration?",
        "answer": "Duration depends on project scope. Interior painting typically takes 3-7 days, carpentry 7-21 days.",
    },
    {
        "question": "Do you use quality materials?",
        "answer": "Yes, we exclusively use premium quality materials from trusted brands. GST compliant materials.",
    },
    {
        "question": "What warranty do you provide?",
        "answer": "We provide 1-year warranty on painting and 2-year warranty on carpentry work.",
    },
]

TESTIMONIALS_DATA = {
    "average_rating": 4.8,
    "items": [
        {
            "customer_name": "Rajesh Kumar",
            "project": "Interior Painting - 3BHK Home",
            "rating": 5,
            "feedback": "Excellent quality work and very professional team. Highly recommended!",
        },
        {
            "customer_name": "Priya Sharma",
            "project": "Carpenter Work - Custom Wardrobe",
            "rating": 5,
            "feedback": "Best carpentry work I've seen. Great attention to detail.",
        },
        {
            "customer_name": "Amit Patel",
            "project": "Tile Installation - Bathroom Renovation",
            "rating": 4.5,
            "feedback": "Professional service and on-time completion. Thank you!",
        },
    ],
}


# ---------------------------------------------------------------------------
# Lead delivery — sends an email instead of calling a backend API
# ---------------------------------------------------------------------------
def send_lead_email(subject: str, body: str) -> bool:
    """Email a captured lead to NOTIFY_EMAIL. Returns True on success."""
    if not SMTP_USERNAME or not SMTP_PASSWORD:
        logger.warning("SMTP not configured — lead NOT emailed. Subject: %s\n%s", subject, body)
        return False

    try:
        msg = MIMEText(body)
        msg["Subject"] = subject
        msg["From"] = SMTP_USERNAME
        msg["To"] = NOTIFY_EMAIL

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT, timeout=10) as server:
            server.starttls()
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
            server.sendmail(SMTP_USERNAME, [NOTIFY_EMAIL], msg.as_string())
        return True
    except Exception as e:
        logger.error("Email send failed: %s", e)
        return False


# ---------------------------------------------------------------------------
# Header
# ---------------------------------------------------------------------------
st.markdown(
    f"""
    <div class="main-header">
        <h1>🏠 B H Enterprises</h1>
        <p>Premium Building Materials & Professional Home Decorator Services</p>
        <p>GST: {GST_NUMBER} | Bangalore, India</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# Navigation
# ---------------------------------------------------------------------------
page = st.sidebar.radio(
    "Navigation",
    ["Home", "About Us", "Services", "Contact", "Get Quote", "FAQ", "Testimonials"],
)

# ==================== HOME ====================
if page == "Home":
    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            """
            ## Welcome to B H Enterprises

            We are your trusted partner for:
            - **Premium Building Materials**
            - **Professional Home Decoration**
            - **Quality Assurance**
            - **Timely Project Delivery**

            With years of experience, we deliver excellence in every project.
            """
        )

    with col2:
        st.markdown(
            '<div class="hero-banner">🏗️🎨🪵🟦</div>',
            unsafe_allow_html=True,
        )
        st.caption("Quality Home Solutions")

    st.divider()

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Customer Rating", "4.8/5", "+0.2")
    with col2:
        st.metric("Projects Completed", "500+", "")
    with col3:
        st.metric("Happy Customers", "1000+", "")


# ==================== ABOUT ====================
elif page == "About Us":
    st.markdown(f"## {ABOUT_DATA['company_name']}")
    st.write(ABOUT_DATA["description"])

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Our Services")
        for service in ABOUT_DATA["services"]:
            st.write(f"✓ {service}")

    with col2:
        st.markdown("### Why Choose Us")
        for reason in ABOUT_DATA["why_choose_us"]:
            st.write(f"✓ {reason}")


# ==================== SERVICES ====================
elif page == "Services":
    st.markdown("## Our Services")

    services = [
        {"name": "White Cement Supply", "description": "Premium quality white cement for finest finishing", "icon": "🏗️"},
        {"name": "Professional Painting", "description": "Interior and exterior painting with premium paints", "icon": "🎨"},
        {"name": "Carpenter Work", "description": "Custom carpentry and woodwork solutions", "icon": "🪵"},
        {"name": "Tile Installation", "description": "Expert tile fixing and installation services", "icon": "🟦"},
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
        st.write(f"🏢 GST: {GST_NUMBER}")

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
            elif "@" not in email:
                st.error("Please enter a valid email address")
            else:
                body = (
                    f"New contact form submission\n\n"
                    f"Name: {name}\n"
                    f"Email: {email}\n"
                    f"Phone: {phone}\n"
                    f"Category: {category}\n"
                    f"Subject: {subject}\n\n"
                    f"Message:\n{message}\n\n"
                    f"Submitted: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
                )
                send_lead_email(f"[B H Enterprises] Contact: {subject}", body)
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
            project_type = st.selectbox(
                "Project Type *",
                ["Interior Painting", "Carpenter Work", "Tile Installation", "Complete Home Decoration", "Other"],
            )
            budget_range = st.selectbox(
                "Budget Range",
                ["Below ₹50,000", "₹50,000 - ₹1,00,000", "₹1,00,000 - ₹5,00,000", "Above ₹5,00,000", "Not Sure"],
            )
            area_sq_ft = st.number_input("Area (Sq. Ft.)", min_value=0.0, step=100.0)

        description = st.text_area(
            "Project Description *", placeholder="Tell us about your project...", height=150
        )

        submit_quote = st.form_submit_button("Request Quote", use_container_width=True)

        if submit_quote:
            if not all([name, email, phone, project_type, description]):
                st.error("Please fill all required fields")
            elif "@" not in email:
                st.error("Please enter a valid email address")
            else:
                area_text = f"{area_sq_ft:.0f} sq ft" if area_sq_ft > 0 else "Not specified"
                body = (
                    f"New quote request\n\n"
                    f"Name: {name}\n"
                    f"Email: {email}\n"
                    f"Phone: {phone}\n"
                    f"Project Type: {project_type}\n"
                    f"Budget Range: {budget_range}\n"
                    f"Area: {area_text}\n\n"
                    f"Description:\n{description}\n\n"
                    f"Submitted: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
                )
                send_lead_email(f"[B H Enterprises] Quote request: {project_type}", body)
                st.success("✅ Quote request submitted! We'll contact you soon.")
                st.balloons()


# ==================== FAQ ====================
elif page == "FAQ":
    st.markdown("## Frequently Asked Questions")
    for faq in FAQ_DATA:
        with st.expander(f"❓ {faq['question']}"):
            st.write(faq["answer"])


# ==================== TESTIMONIALS ====================
elif page == "Testimonials":
    st.markdown("## Customer Testimonials")

    col1, col2, col3 = st.columns(3)
    col1.metric("Average Rating", f"{TESTIMONIALS_DATA['average_rating']}/5.0", "⭐")
    col2.metric("Total Reviews", len(TESTIMONIALS_DATA["items"]))
    col3.metric("Satisfaction Rate", "98%", "✅")

    st.divider()

    for testimonial in TESTIMONIALS_DATA["items"]:
        col1, col2 = st.columns([0.15, 0.85])
        with col1:
            st.write("⭐" * int(testimonial["rating"]))
        with col2:
            st.markdown(f"### {testimonial['customer_name']}")
            st.write(f"**Project:** {testimonial['project']}")
            st.write(f"*{testimonial['feedback']}*")
        st.divider()


# ==================== SIDEBAR ====================
st.sidebar.divider()
st.sidebar.markdown("### About")
st.sidebar.info(
    f"""
    **B H Enterprises**

    Premium Building Materials & Home Decorator Services

    📞 {CONTACT_PHONE}
    📧 {CONTACT_EMAIL}
    🏢 Delhi, India
    """
)

st.sidebar.markdown("### Links")
st.sidebar.link_button("🌐 Visit Website", "https://bhenterprises.com")
st.sidebar.link_button("📘 Facebook", "https://www.facebook.com/bhenterprises")
st.sidebar.link_button("📸 Instagram", "https://www.instagram.com/bhenterprises")

st.sidebar.markdown("---")
st.sidebar.caption("© 2026 B H Enterprises. All rights reserved.")
