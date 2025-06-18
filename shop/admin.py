from django.contrib import admin
from .models import Category, Product, ProductImage, Order, OrderItem, Cart, CartItem, ProductReview, TeamMember, Discount, Testimonial

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'created_at']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name', 'description']

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    fields = ('image', 'is_primary', 'created_at')
    readonly_fields = ('created_at',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'discount_percentage', 'get_discounted_price_display', 'stock', 'available', 'views_count', 'get_trending_score_display', 'created_at']
    list_filter = ['available', 'created_at', 'category', 'material', 'is_featured']
    list_editable = ['price', 'discount_percentage', 'stock', 'available']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name', 'description']
    inlines = [ProductImageInline]
    readonly_fields = ['created_at', 'updated_at', 'views_count', 'last_viewed', 'get_trending_score_display']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'category', 'description', 'is_featured')
        }),
        ('Pricing & Stock', {
            'fields': ('price', 'stock', 'available')
        }),
        ('Discount Settings', {
            'fields': ('discount_percentage', 'discount_start_date', 'discount_end_date'),
            'classes': ('collapse',),
            'description': 'Set discount percentage and optional start/end dates for the discount period.'
        }),
        ('Product Details', {
            'fields': ('material', 'weight', 'dimensions')
        }),
        ('Analytics', {
            'fields': ('views_count', 'last_viewed', 'get_trending_score_display'),
            'classes': ('collapse',),
            'description': 'Analytics data for trending calculations.'
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_discounted_price_display(self, obj):
        """Display discounted price in admin list."""
        if obj.is_discount_active():
            return f"₹{obj.get_discounted_price():.2f} (-{obj.discount_percentage}%)"
        return f"₹{obj.price:.2f}"
    get_discounted_price_display.short_description = 'Price (with discount)'

    def get_trending_score_display(self, obj):
        """Display trending score in admin list."""
        score = obj.get_trending_score()
        if score >= 5.0:
            return f"{score} 🔥"
        return f"{score}"
    get_trending_score_display.short_description = 'Trending Score'

@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    list_display = ['name', 'discount_percentage', 'is_active', 'show_on_homepage', 'created_at']
    list_filter = ['is_active', 'show_on_homepage']
    search_fields = ['name']
    list_editable = ['is_active', 'show_on_homepage']
    readonly_fields = ['created_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'discount_percentage')
        }),
        ('Settings', {
            'fields': ('is_active', 'show_on_homepage')
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'first_name', 'last_name', 'email', 'status', 'total_amount', 'created_at']
    list_filter = ['status', 'created_at', 'payment_status']
    search_fields = ['first_name', 'last_name', 'email', 'address', 'tracking_number']
    inlines = [OrderItemInline]
    readonly_fields = ['created_at', 'updated_at']

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'created_at', 'updated_at']
    search_fields = ['user__username', 'user__email']

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['cart', 'product', 'quantity']
    list_filter = ['cart__user']
    search_fields = ['product__name', 'cart__user__username']

@admin.register(ProductReview)
class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ['product', 'user', 'rating', 'is_approved', 'created_at']
    list_filter = ['is_approved', 'rating', 'created_at']
    search_fields = ['product__name', 'user__username', 'comment']
    list_editable = ['is_approved']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ['name', 'position', 'order', 'is_active']
    list_filter = ['is_active']
    search_fields = ['name', 'position', 'bio']
    list_editable = ['order', 'is_active']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ['name', 'location', 'rating', 'is_active', 'order', 'created_at']
    list_filter = ['rating', 'is_active']
    search_fields = ['name', 'location', 'comment']
    list_editable = ['is_active', 'order']
    readonly_fields = ['created_at']
    
    fieldsets = (
        ('Customer Information', {
            'fields': ('name', 'location', 'rating')
        }),
        ('Testimonial', {
            'fields': ('comment',)
        }),
        ('Settings', {
            'fields': ('is_active', 'order')
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
