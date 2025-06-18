from django import forms
from .models import ProductReview

class ProductReviewForm(forms.ModelForm):
    rating = forms.ChoiceField(
        choices=ProductReview.RATING_CHOICES,
        widget=forms.RadioSelect(attrs={'class': 'star-rating'}),
        required=True
    )
    comment = forms.CharField(
        widget=forms.Textarea(attrs={
            'rows': 4,
            'placeholder': 'Write your review here (optional)...',
            'class': 'form-control'
        }),
        required=False
    )

    class Meta:
        model = ProductReview
        fields = ['rating', 'comment'] 