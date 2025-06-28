from django.urls import path
from .views import BookListView,BookDetailView,ReviewUpdateView,DeleteReviewView

app_name='books'
urlpatterns = [
    path('', BookListView.as_view(), name='book_list'),
    path('<int:id>/', BookDetailView.as_view(), name='book_detail'),
    path('<int:bid>/reviews/<int:rid>/edit/', ReviewUpdateView.as_view(), name='book_update'),
    path('<int:bid>/reviews/<int:rid>/delete/', DeleteReviewView.as_view(), name='book_delete'),
]



