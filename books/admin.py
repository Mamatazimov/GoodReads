from django.contrib import admin

from .models import Book, Author, BookAuthor, BookReview

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'isbn', 'discription')
    search_fields = ('title', 'isbn')
    ordering = ('title',)

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email')
    search_fields = ('first_name', 'last_name', 'email')
    ordering = ('last_name', 'first_name')

@admin.register(BookAuthor)
class BookAuthorAdmin(admin.ModelAdmin):
    list_display = ('book', 'author')
    search_fields = ('book__title', 'author__first_name', 'author__last_name')
    ordering = ('book__title', 'author__last_name')

@admin.register(BookReview)
class BookReviewAdmin(admin.ModelAdmin):
    list_display = ('book', 'user', 'rating')
    search_fields = ('book__title', 'user__username', 'review_text')
    ordering = ('-rating', 'book__title')
    list_filter = ('rating',)

