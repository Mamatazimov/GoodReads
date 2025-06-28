from django import forms

from books.models import BookReview


class ReviewForm(forms.ModelForm):
    review_text = forms.CharField(widget=forms.Textarea(attrs={'class':"form-control mb-3","style":"height:5rem;","placeholder":"Comment"}))
    rating = forms.IntegerField(max_value=5, min_value=1,widget=forms.NumberInput(attrs={'class':"form-control mb-3","placeholder":"Rating"}))
    class Meta:
        model=BookReview
        fields=("review_text","rating")

