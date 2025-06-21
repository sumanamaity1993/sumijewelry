from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from decimal import Decimal
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from datetime import timedelta
from django.db.models import Count, Avg
from django.db import transaction
from django.db.models import F

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='categories/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Jewelry specific fields
    material = models.CharField(max_length=100)  # e.g., Gold, Silver, Platinum
    weight = models.DecimalField(max_digits=6, decimal_places=2, help_text='Weight in grams')
    dimensions = models.CharField(max_length=50, blank=True, help_text='Dimensions in mm')
    is_featured = models.BooleanField(default=False)
    
    # Analytics fields for trending
    views_count = models.PositiveIntegerField(default=0, help_text='Number of times product was viewed')
    last_viewed = models.DateTimeField(null=True, blank=True, help_text='Last time product was viewed')
    
    # Discount fields
    discount_percentage = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        default=0, 
        help_text='Discount percentage (0-100)'
    )
    discount_start_date = models.DateTimeField(
        blank=True, 
        null=True, 
        help_text='Start date for discount (optional)'
    )
    discount_end_date = models.DateTimeField(
        blank=True, 
        null=True, 
        help_text='End date for discount (optional)'
    )

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['id', 'slug']),
            models.Index(fields=['name']),
            models.Index(fields=['-created_at']),
        ]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        # Automatically set available status based on stock
        self.available = self.stock > 0
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_detail', args=[self.slug])

    def get_primary_image(self):
        """Get the primary image or first available image for the product."""
        primary = self.images.filter(is_primary=True).first()
        if primary:
            return primary.image
        return self.images.first().image if self.images.exists() else None

    def is_discount_active(self):
        """Check if discount is currently active based on dates."""
        now = timezone.now()
        
        # Check if discount percentage is greater than 0
        if self.discount_percentage <= 0:
            return False
        
        # Check start date
        if self.discount_start_date and now < self.discount_start_date:
            return False
        
        # Check end date
        if self.discount_end_date and now > self.discount_end_date:
            return False
        
        return True

    def get_discounted_price(self):
        """Get the discounted price if discount is active."""
        if self.is_discount_active():
            discount_amount = (self.price * self.discount_percentage) / 100
            return self.price - discount_amount
        return self.price

    def get_discount_amount(self):
        """Get the discount amount in currency."""
        if self.is_discount_active():
            return (self.price * self.discount_percentage) / 100
        return 0

    def get_discount_savings_percentage(self):
        """Get the discount percentage for display."""
        if self.is_discount_active():
            return self.discount_percentage
        return 0

    def increment_views(self):
        """Increment the view count and update last viewed timestamp."""
        with transaction.atomic():
            # Use F() expression to avoid race conditions
            Product.objects.filter(id=self.id).update(
                views_count=F('views_count') + 1,
                last_viewed=timezone.now()
            )
            # Refresh the object from database
            self.refresh_from_db()

    def get_trending_score(self):
        """Calculate trending score based on views, reviews, and recent activity."""
        # Get review count and average rating
        reviews_data = self.reviews.filter(is_approved=True).aggregate(
            review_count=Count('id'),
            avg_rating=Avg('rating')
        )
        
        review_count = reviews_data['review_count'] or 0
        avg_rating = reviews_data['avg_rating'] or 0
        
        # Get recent order count (last 30 days)
        thirty_days_ago = timezone.now() - timedelta(days=30)
        recent_orders = OrderItem.objects.filter(
            product=self,
            order__created_at__gte=thirty_days_ago,
            order__status__in=['delivered', 'shipped']
        ).count()
        
        # Calculate trending score
        # Formula: (views * 0.3) + (reviews * 0.4) + (recent_orders * 0.3) + (avg_rating * 0.2)
        trending_score = (
            (self.views_count * 0.3) +
            (review_count * 0.4) +
            (recent_orders * 0.3) +
            (avg_rating * 0.2)
        )
        
        return round(trending_score, 2)

    def is_new_arrival(self):
        """Check if product is a new arrival (created in last 7 days)."""
        seven_days_ago = timezone.now() - timedelta(days=7)
        return self.created_at >= seven_days_ago

    def is_trending(self):
        """Check if product is trending based on trending score."""
        return self.get_trending_score() >= 2.0  # Lower threshold for trending badge

class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/')
    is_primary = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-is_primary', '-created_at']

    def __str__(self):
        return f'Image for {self.product.name}'

    def save(self, *args, **kwargs):
        # If this image is set as primary, unset any other primary images
        if self.is_primary:
            ProductImage.objects.filter(product=self.product, is_primary=True).exclude(id=self.id).update(is_primary=False)
        super().save(*args, **kwargs)

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]

    PAYMENT_METHOD_CHOICES = [
        ('upi', 'UPI'),
        ('cod', 'Cash on Delivery'),
        ('credit_card', 'Credit Card'),
        ('debit_card', 'Debit Card'),
        ('net_banking', 'Net Banking'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    address = models.TextField()
    phone = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_status = models.BooleanField(default=False)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, default='upi')
    tracking_number = models.CharField(max_length=50, blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'Order {self.id}'

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'{self.quantity} x {self.product.name}'

    def get_cost(self):
        return self.price * self.quantity

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Cart {self.id} - {self.user.username}'

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())
    
    def get_total_items(self):
        return sum(item.quantity for item in self.items.all())

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=0,
        help_text='Price at the time of adding to cart'
    )

    def __str__(self):
        return f'{self.quantity} x {self.product.name}'

    def get_cost(self):
        return self.price * self.quantity

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone_number = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s profile"

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class ProductReview(models.Model):
    RATING_CHOICES = [
        (1, '1 Star'),
        (2, '2 Stars'),
        (3, '3 Stars'),
        (4, '4 Stars'),
        (5, '5 Stars'),
    ]

    product = models.ForeignKey(Product, related_name='reviews', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=RATING_CHOICES)
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_approved = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']
        unique_together = ['product', 'user']  # One review per user per product

    def __str__(self):
        return f'Review by {self.user.username} for {self.product.name}'

    def get_rating_display(self):
        return '★' * self.rating + '☆' * (5 - self.rating)

class TeamMember(models.Model):
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    bio = models.TextField()
    image = models.ImageField(upload_to='team/')
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', 'name']

    def __str__(self):
        return self.name

class Discount(models.Model):
    name = models.CharField(max_length=100, help_text="Simple name like 'Summer Sale' or 'New Customer Discount'")
    discount_percentage = models.IntegerField(
        help_text="Discount percentage (e.g., 20 for 20% off)",
        validators=[MinValueValidator(1), MaxValueValidator(100)]
    )
    is_active = models.BooleanField(default=True)
    show_on_homepage = models.BooleanField(default=True, help_text="Show this discount on homepage")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} ({self.discount_percentage}% off)"

    def get_display_text(self):
        """Get formatted display text for the discount."""
        return f"{self.discount_percentage}% OFF"

class Testimonial(models.Model):
    name = models.CharField(max_length=100, help_text="Customer name")
    location = models.CharField(max_length=100, help_text="Customer location (e.g., Mumbai, Delhi)")
    rating = models.IntegerField(
        choices=[(i, f'{i} Star{"s" if i != 1 else ""}') for i in range(1, 6)],
        default=5,
        help_text="Customer rating (1-5 stars)"
    )
    comment = models.TextField(help_text="Customer testimonial/review")
    is_active = models.BooleanField(default=True, help_text="Show this testimonial on homepage")
    order = models.PositiveIntegerField(default=0, help_text="Display order (lower numbers show first)")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', '-created_at']

    def __str__(self):
        return f"{self.name} - {self.location} ({self.rating}★)"

    def get_rating_display(self):
        """Get star rating display."""
        return '★' * self.rating + '☆' * (5 - self.rating)
