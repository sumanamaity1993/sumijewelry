from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Avg, Count, F, Q
from django.core.paginator import Paginator
from .models import Category, Product, Order, OrderItem, Cart, CartItem, ProductReview, TeamMember, Discount, Testimonial
from django.views.decorators.http import require_POST
from django.contrib.auth.forms import PasswordChangeForm, SetPasswordForm
from allauth.account.forms import AddEmailForm
from allauth.socialaccount.forms import DisconnectForm
from django.contrib.admin.views.decorators import staff_member_required
from django.http import JsonResponse
from .forms import ProductReviewForm
from datetime import timedelta
from django.utils import timezone
from django.db import models

def home(request):
    """Home page view showing featured products and categories."""
    featured_products = Product.objects.filter(is_featured=True, available=True)[:8]
    
    # New Arrivals - Products created in the last 7 days
    seven_days_ago = timezone.now() - timedelta(days=7)
    new_arrivals = Product.objects.filter(
        available=True, 
        created_at__gte=seven_days_ago
    ).order_by('-created_at')[:4]
    
    # Trending Products - Based on sophisticated analytics (views, reviews, recent orders)
    trending_products = Product.objects.filter(
        available=True
    ).annotate(
        trending_score=models.F('views_count') * 0.3 + 
                      models.Count('reviews', filter=models.Q(reviews__is_approved=True)) * 0.4 +
                      models.Count('orderitem', filter=models.Q(
                          orderitem__order__created_at__gte=timezone.now() - timedelta(days=30),
                          orderitem__order__status__in=['delivered', 'shipped']
                      )) * 0.3 +
                      models.Avg('reviews__rating', filter=models.Q(reviews__is_approved=True)) * 0.2
    ).filter(
        trending_score__gt=0  # Only show products with some trending activity
    ).order_by('-trending_score')[:4]  # Show top 4 trending products on home page
    
    categories = Category.objects.all()[:6]
    
    # Get active discounts
    active_discounts = Discount.objects.filter(
        is_active=True,
        show_on_homepage=True
    )[:3]  # Show up to 3 active discounts
    
    # Get active testimonials
    testimonials = Testimonial.objects.filter(is_active=True)[:3]
    
    return render(request, 'shop/home.html', {
        'featured_products': featured_products,
        'new_arrivals': new_arrivals,
        'trending_products': trending_products,
        'categories': categories,
        'testimonials': testimonials,
        'active_discounts': active_discounts,
    })

def team(request):
    """View for displaying team members."""
    team_members = TeamMember.objects.filter(is_active=True)
    return render(request, 'shop/team.html', {
        'team_members': team_members,
    })

def product_list(request, category_slug=None):
    """View for listing products, optionally filtered by category."""
    category = None
    categories = Category.objects.all()
    products = Product.objects.all()  # Show all products, including out-of-stock ones
    
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    
    # Search functionality
    query = request.GET.get('q')
    if query:
        products = products.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(material__icontains=query)
        )
    
    # Material filter
    material = request.GET.get('material')
    if material:
        products = products.filter(material=material)
    
    # Price range filter
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    
    if min_price:
        try:
            min_price = float(min_price)
            products = products.filter(price__gte=min_price)
        except ValueError:
            pass
    
    if max_price:
        try:
            max_price = float(max_price)
            products = products.filter(price__lte=max_price)
        except ValueError:
            pass
    
    # Sorting
    sort_by = request.GET.get('sort', 'newest')
    print(f"Sort by: {sort_by}")  # Debug print
    if sort_by == 'price_low':
        products = products.order_by('price')
        print("Sorting by price low to high")
    elif sort_by == 'price_high':
        products = products.order_by('-price')
        print("Sorting by price high to low")
    elif sort_by == 'newest':
        products = products.order_by('-created_at')
        print("Sorting by newest")
    else:
        products = products.order_by('-created_at')  # Default to newest
        print("Default sorting by newest")
    
    print(f"Final query: {products.query}")  # Debug print
    
    # Pagination
    paginator = Paginator(products, 12)  # Show 12 products per page
    page = request.GET.get('page')
    products = paginator.get_page(page)
    
    return render(request, 'shop/product_list.html', {
        'category': category,
        'categories': categories,
        'products': products,
    })

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    
    # Track product view for analytics
    print(f"Before increment: Product '{product.name}' has {product.views_count} views")
    product.increment_views()
    print(f"After increment: Product '{product.name}' now has {product.views_count} views")
    
    cart_item = None
    if request.user.is_authenticated:
        cart_item = CartItem.objects.filter(
            cart__user=request.user,
            product=product
        ).first()
    
    # Get approved reviews and calculate average rating
    reviews = product.reviews.filter(is_approved=True)
    avg_rating = reviews.aggregate(Avg('rating'))['rating__avg'] or 0
    
    # Check if user has purchased the product
    has_purchased = False
    if request.user.is_authenticated:
        has_purchased = OrderItem.objects.filter(
            order__user=request.user,
            order__status='delivered',
            product=product
        ).exists()
    
    # Get user's existing review if any
    user_review = None
    if request.user.is_authenticated:
        user_review = ProductReview.objects.filter(
            product=product,
            user=request.user
        ).first()
    
    # Handle review submission
    review_form = None
    if request.user.is_authenticated and has_purchased:
        if not user_review:
            review_form = ProductReviewForm()
            if request.method == 'POST':
                review_form = ProductReviewForm(request.POST)
                if review_form.is_valid():
                    review = review_form.save(commit=False)
                    review.product = product
                    review.user = request.user
                    review.save()
                    messages.success(request, 'Your review has been submitted and is pending approval.')
                    return redirect('shop:product_detail', slug=product.slug)
        else:
            messages.info(request, 'You have already reviewed this product.')
    
    context = {
        'product': product,
        'cart_item': cart_item,
        'reviews': reviews,
        'avg_rating': avg_rating,
        'review_form': review_form,
        'has_purchased': has_purchased,
        'user_review': user_review,
    }
    return render(request, 'shop/product_detail.html', context)

@login_required
def cart_detail(request):
    """View for displaying the shopping cart."""
    cart, created = Cart.objects.get_or_create(user=request.user)
    return render(request, 'shop/cart_detail.html', {'cart': cart})

@login_required
def cart_add(request, product_id):
    """View for adding a product to the cart."""
    product = get_object_or_404(Product, id=product_id, available=True)
    cart, created = Cart.objects.get_or_create(user=request.user)
    
    # Get the current price (discounted if available)
    current_price = product.get_discounted_price()
    
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart, 
        product=product,
        defaults={'price': current_price}
    )
    
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    
    messages.success(request, f'{product.name} added to cart.')
    return redirect('shop:cart_detail')

@login_required
def cart_remove(request, product_id):
    """View for removing a product from the cart."""
    cart = get_object_or_404(Cart, user=request.user)
    product = get_object_or_404(Product, id=product_id)
    cart_item = get_object_or_404(CartItem, cart=cart, product=product)
    cart_item.delete()
    
    messages.success(request, f'{product.name} removed from cart.')
    return redirect('shop:cart_detail')

@login_required
def cart_update(request, product_id):
    """View for updating cart item quantity."""
    cart = get_object_or_404(Cart, user=request.user)
    product = get_object_or_404(Product, id=product_id)
    cart_item = get_object_or_404(CartItem, cart=cart, product=product)
    
    quantity = int(request.POST.get('quantity', 1))
    if quantity > 0:
        cart_item.quantity = quantity
        cart_item.save()
        messages.success(request, f'Cart updated.')
    else:
        cart_item.delete()
        messages.success(request, f'{product.name} removed from cart.')
    
    return redirect('shop:cart_detail')

def update_product_stock(product, quantity, increase=False):
    """Helper function to update product stock."""
    if increase:
        product.stock += quantity
    else:
        if product.stock < quantity:
            raise ValueError(f'Not enough stock for {product.name}')
        product.stock -= quantity
    product.save()

@login_required
def checkout(request):
    """View for the checkout process."""
    cart = get_object_or_404(Cart, user=request.user)
    if not cart.items.exists():
        messages.warning(request, 'Your cart is empty.')
        return redirect('shop:cart_detail')
    
    if request.method == 'POST':
        try:
            # First check if all items are in stock
            for item in cart.items.all():
                if item.product.stock < item.quantity:
                    messages.error(request, f'Sorry, {item.product.name} is out of stock.')
                    return redirect('shop:cart_detail')
            
            total = cart.get_total_cost()
            shipping_fee = 0 if total >= 999 else 100
            total_amount = total + shipping_fee
            
            # Create order
            order = Order.objects.create(
                user=request.user,
                first_name=request.POST.get('first_name'),
                last_name=request.POST.get('last_name'),
                email=request.POST.get('email'),
                address=request.POST.get('address'),
                phone=request.POST.get('phone'),
                total_amount=total_amount,
                payment_method=request.POST.get('payment_method', 'credit_card'),
                payment_status=request.POST.get('payment_method') == 'credit_card'
            )
            
            # Create order items and update inventory
            for item in cart.items.all():
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    price=item.product.price,
                    quantity=item.quantity
                )
                # Update product stock
                update_product_stock(item.product, item.quantity)
            
            # Clear the cart
            cart.items.all().delete()
            
            messages.success(request, 'Your order has been placed successfully!')
            return redirect('shop:order_detail', order_id=order.id)
            
        except ValueError as e:
            messages.error(request, str(e))
            return redirect('shop:cart_detail')
        except Exception as e:
            messages.error(request, 'An error occurred while processing your order. Please try again.')
            return redirect('shop:cart_detail')
    
    return render(request, 'shop/checkout.html', {'cart': cart})

@login_required
def order_list(request):
    """View for listing user's orders."""
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'shop/order_list.html', {'orders': orders})

@login_required
def order_detail(request, order_id):
    """View for displaying order details."""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'shop/order_detail.html', {'order': order})

def search(request):
    """View for searching products."""
    query = request.GET.get('q', '')
    products = Product.objects.all()  # Show all products, including out-of-stock ones
    
    if query:
        products = products.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(material__icontains=query)
        )
    
    # Apply material filter
    material = request.GET.get('material')
    if material:
        products = products.filter(material=material)
    
    # Apply price range filter
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)
    
    # Apply sorting
    sort = request.GET.get('sort', 'newest')
    if sort == 'price_low':
        products = products.order_by('price')
    elif sort == 'price_high':
        products = products.order_by('-price')
    else:  # newest
        products = products.order_by('-created_at')
    
    # Get unique materials for filter options
    materials = Product.objects.values_list('material', flat=True).distinct()
    
    return render(request, 'shop/search_results.html', {
        'products': products,
        'query': query,
        'materials': materials,
    })

@login_required
def profile(request):
    """View for user profile."""
    if request.method == 'POST':
        # Update user information
        user = request.user
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        user.save()
        
        # Update profile information
        profile = user.profile
        profile.phone_number = request.POST.get('phone', profile.phone_number)
        profile.address = request.POST.get('address', profile.address)
        profile.save()
        
        messages.success(request, 'Your profile has been updated successfully!')
        return redirect('shop:profile')
    
    return render(request, 'shop/profile.html')

@login_required
def user_orders(request):
    """View for user's order history."""
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    subtotals = {}
    for order in orders:
        subtotal = sum(item.get_cost() for item in order.items.all())
        subtotals[order.id] = subtotal
    return render(request, 'shop/user_orders.html', {'orders': orders, 'subtotals': subtotals})

@login_required
def user_address(request):
    """View for managing user's shipping addresses."""
    return render(request, 'shop/user_address.html')

@require_POST
@login_required
def cancel_order(request, order_id):
    """View for cancelling an order."""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    if order.status == 'pending':
        try:
            # Restore product stock
            for item in order.items.all():
                update_product_stock(item.product, item.quantity, increase=True)
            
            order.status = 'cancelled'
            order.save()
            messages.success(request, f'Order #{order.id} has been cancelled.')
        except Exception as e:
            messages.error(request, 'An error occurred while cancelling the order. Please try again.')
    else:
        messages.warning(request, 'Only pending orders can be cancelled.')
    return redirect('shop:user_orders')

@login_required
def account_settings(request):
    """View for managing account settings including password, email, and social connections."""
    context = {
        'password_form': PasswordChangeForm(request.user),
        'set_password_form': SetPasswordForm(request.user),
        'add_email_form': AddEmailForm(request.user),
        'disconnect_form': DisconnectForm(request=request),
    }
    return render(request, 'shop/account_settings.html', context)

@require_POST
@staff_member_required
def mark_order_delivered(request, order_id):
    """View for marking an order as delivered (admin only)."""
    order = get_object_or_404(Order, id=order_id)
    if order.status not in ['cancelled']:
        order.status = 'delivered'
        order.save()
        messages.success(request, f'Order #{order.id} has been marked as delivered.')
    else:
        messages.warning(request, 'Cancelled orders cannot be marked as delivered.')
    return redirect('shop:order_detail', order_id=order.id)

def trending_products(request):
    """View for displaying top trending products."""
    # Get top 10 trending products based on sophisticated analytics
    trending_products = Product.objects.filter(
        available=True
    ).annotate(
        trending_score=models.F('views_count') * 0.3 + 
                      models.Count('reviews', filter=models.Q(reviews__is_approved=True)) * 0.4 +
                      models.Count('orderitem', filter=models.Q(
                          orderitem__order__created_at__gte=timezone.now() - timedelta(days=30),
                          orderitem__order__status__in=['delivered', 'shipped']
                      )) * 0.3 +
                      models.Avg('reviews__rating', filter=models.Q(reviews__is_approved=True)) * 0.2
    ).filter(
        trending_score__gt=0  # Only show products with some trending activity
    ).order_by('-trending_score')[:10]  # Show top 10 trending products
    
    return render(request, 'shop/trending_products.html', {
        'trending_products': trending_products,
    })
