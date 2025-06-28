from django.urls import path

from api.views import ApiBookReviewView,ApiAllBookReviewView

app_name = 'api'
urlpatterns = [
    path('books/review/<int:id>/',ApiBookReviewView.as_view(),name='api-book_review'),
    path('books/review/',ApiAllBookReviewView.as_view(),name='api-all_book_review'),
]