from rest_framework import serializers
from django.contrib.auth.models import User

from books.models import BookReview, Book



class ApiUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', "first_name", "last_name", 'email']

class ApiBooksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title',"discription","isbn"]

class ApiReviewSerializer(serializers.ModelSerializer):
    user=ApiUserSerializer(read_only=True)
    book=ApiBooksSerializer(read_only=True)
    book_id=serializers.IntegerField(write_only=True)
    user_id=serializers.IntegerField(write_only=True)

    class Meta:
        model = BookReview
        fields = ["id","user","book","review_text","rating","created_at","book_id","user_id"]




