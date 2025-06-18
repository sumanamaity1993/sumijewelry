from django import template
from django.db.models import Avg
from decimal import Decimal
from django.template.defaultfilters import stringfilter
from django.template.context import Context

register = template.Library()

@register.filter
def indian_currency(value):
    """Format value as Indian currency."""
    try:
        value = float(value)
        return f"{value:,.2f}"
    except (ValueError, TypeError):
        return value

@register.filter
def dict_get(dictionary, key):
    """Get a value from a dictionary using a key."""
    return dictionary.get(key) 

@register.filter
def multiply(value, arg):
    """Multiply the value by the argument."""
    try:
        return str(value) * int(arg)
    except (ValueError, TypeError):
        return ''

@register.filter
def subtract(value, arg):
    """Subtract the arg from the value."""
    try:
        return float(value) - float(arg)
    except (ValueError, TypeError):
        return value

@register.filter
def avg_rating(reviews):
    """Calculate average rating from reviews."""
    if not reviews:
        return 0
    # Use the same calculation as in the product detail view
    avg = reviews.aggregate(Avg('rating'))['rating__avg']
    return avg if avg is not None else 0

@register.filter
def filter_reviews(reviews, context=None):
    """
    Filter reviews to show approved reviews and user's own reviews.
    The context parameter is automatically provided by Django.
    """
    if not reviews:
        return reviews
    
    # Get the request from the context
    request = None
    if context:
        request = context.get('request')
    
    # If user is authenticated, show their reviews and approved reviews
    if request and request.user.is_authenticated:
        return reviews.filter(is_approved=True) | reviews.filter(user=request.user)
    
    # Otherwise, only show approved reviews
    return reviews.filter(is_approved=True) 