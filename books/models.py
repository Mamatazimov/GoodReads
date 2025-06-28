from django.contrib.auth.password_validation import MinimumLengthValidator
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils import timezone


class Book(models.Model):
    title = models.CharField(max_length=160)
    discription = models.TextField(blank=True)
    isbn = models.CharField(max_length=17, unique=True)
    cover_img = models.ImageField(default='cover.png')

    def __str__(self):
        return self.title



class Author(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(blank=True)
    bio = models.TextField(blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    


class BookAuthor(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)


    def __str__(self):
        return f"{self.book.title} by {self.author.first_name} {self.author.last_name}"
    

class BookReview(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    review_text = models.TextField()
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Review for {self.book.title} - Rating: {self.rating}"
    
