"""Contact and lead generation API routes."""

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
import structlog

logger = structlog.get_logger()
router = APIRouter()


class ContactForm(BaseModel):
    """Contact form submission model."""
    name: str = Field(..., min_length=2, max_length=100)
    email: str
    phone: str = Field(..., min_length=10, max_length=15)
    subject: str = Field(..., min_length=5, max_length=200)
    message: str = Field(..., min_length=10, max_length=1000)
    category: Optional[str] = Field(None, description="products, services, or general")


class QuoteRequest(BaseModel):
    """Quote request model for custom requirements."""
    name: str
    email: str
    phone: str
    project_type: str
    description: str
    budget_range: Optional[str] = None
    area_sq_ft: Optional[float] = None


@router.post("/submit")
async def submit_contact_form(form: ContactForm):
    """Submit a contact form - high priority for lead generation."""
    contact_record = {
        "contact_id": f"CT-{form.phone}",
        "name": form.name,
        "email": form.email,
        "phone": form.phone,
        "subject": form.subject,
        "message": form.message,
        "category": form.category or "general",
        "status": "received",
        "response_message": "Thank you for contacting B H Enterprises. We will get back to you within 24 hours.",
    }
    
    logger.info(
        "contact_form_submitted",
        contact_id=contact_record["contact_id"],
        email=form.email,
        category=form.category,
    )
    
    # TODO: Send email notification to admin and confirmation to customer
    # TODO: Save to database
    
    return contact_record


@router.post("/quote-request")
async def request_quote(quote: QuoteRequest):
    """Request a custom quote for specific projects."""
    quote_record = {
        "quote_id": f"QT-{quote.phone}",
        "name": quote.name,
        "email": quote.email,
        "phone": quote.phone,
        "project_type": quote.project_type,
        "description": quote.description,
        "budget_range": quote.budget_range,
        "area_sq_ft": quote.area_sq_ft,
        "status": "pending_review",
        "message": "Your quote request has been received. Our team will prepare a detailed quote and send it to you soon.",
    }
    
    logger.info(
        "quote_requested",
        quote_id=quote_record["quote_id"],
        email=quote.email,
        project_type=quote.project_type,
    )
    
    # TODO: Send email notification to team and customer
    # TODO: Save to database for follow-up
    
    return quote_record


@router.get("/faq")
async def get_faq():
    """Get frequently asked questions."""
    faqs = [
        {
            "id": 1,
            "question": "What areas do you service?",
            "answer": "We provide services across Bangalore and surrounding areas. Contact us for specific location queries.",
        },
        {
            "id": 2,
            "question": "How do you provide quotes?",
            "answer": "We provide customized quotes after assessing the project on-site. You can request a quote through our form.",
        },
        {
            "id": 3,
            "question": "What is the typical project duration?",
            "answer": "Duration depends on project scope. Interior painting typically takes 3-7 days, carpentry 7-21 days.",
        },
        {
            "id": 4,
            "question": "Do you use quality materials?",
            "answer": "Yes, we exclusively use premium quality materials from trusted brands. GST compliant materials.",
        },
        {
            "id": 5,
            "question": "What warranty do you provide?",
            "answer": "We provide 1-year warranty on painting and 2-year warranty on carpentry work.",
        },
    ]
    
    logger.info("faq_retrieved", count=len(faqs))
    
    return {
        "faqs": faqs,
        "total": len(faqs),
    }


@router.get("/about")
async def get_about():
    """Get company information for SEO."""
    about_data = {
        "company_name": "B H Enterprises",
        "gst_number": "07ETTPM3697B1Z4",
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
    
    logger.info("about_retrieved")
    
    return about_data


@router.get("/testimonials")
async def get_testimonials():
    """Get customer testimonials for social proof."""
    testimonials = [
        {
            "id": 1,
            "customer_name": "Rajesh Kumar",
            "project": "Interior Painting - 3BHK Home",
            "rating": 5,
            "feedback": "Excellent quality work and very professional team. Highly recommended!",
        },
        {
            "id": 2,
            "customer_name": "Priya Sharma",
            "project": "Carpenter Work - Custom Wardrobe",
            "rating": 5,
            "feedback": "Best carpentry work I've seen. Great attention to detail.",
        },
        {
            "id": 3,
            "customer_name": "Amit Patel",
            "project": "Tile Installation - Bathroom Renovation",
            "rating": 4.5,
            "feedback": "Professional service and on-time completion. Thank you!",
        },
    ]
    
    logger.info("testimonials_retrieved", count=len(testimonials))
    
    return {
        "testimonials": testimonials,
        "average_rating": 4.8,
        "total": len(testimonials),
    }
