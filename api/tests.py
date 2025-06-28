from django.contrib.auth.models import User
from django.template.defaultfilters import title
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from books.models import Book, BookReview


class BookReviewApiViewTest(APITestCase):
    def setUp(self):
        self.usr = User.objects.create_user(username='userbek', email='test@mail.com')
        self.usr.set_password('testpassword123')
        self.usr.save()

    def test_book_review_successful(self):
        book1 = Book.objects.create(title='Book1', discription='Discription1', isbn='121212121212')
        br = BookReview.objects.create(book=book1, user=self.usr, review_text='Very good book',rating=5)
        self.client.force_login(self.usr)


        response = self.client.get(reverse("api:api-book_review", kwargs={'id':br.id}))

        # review
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], br.id)
        self.assertEqual(response.data["review_text"], br.review_text)
        self.assertEqual(response.data["rating"], 5)
        # review user
        self.assertEqual(response.data["user"]["id"],self.usr.id)
        self.assertEqual(response.data["user"]["username"],self.usr.username)
        self.assertEqual(response.data["user"]["first_name"],self.usr.first_name)
        self.assertEqual(response.data["user"]["last_name"],self.usr.last_name)
        self.assertEqual(response.data["user"]["email"],self.usr.email)
        # review book
        self.assertEqual(response.data["book"]["id"],book1.id)
        self.assertEqual(response.data["book"]["title"],book1.title)
        self.assertEqual(response.data["book"]["isbn"],book1.isbn)

    def test_book_review_list_successful(self):
        usr2 = User.objects.create_user(username='userbek2', email='test2@mail.com')
        usr2.set_password('testpassword123')
        usr2.save()

        self.client.force_login(usr2)
        self.client.force_login(self.usr)


        book1 = Book.objects.create(title='Book1', discription='Discription1', isbn='121212121212')
        book2 = Book.objects.create(title='Book2', discription='Discription2', isbn='343434343434')

        b1r1 = BookReview.objects.create(book=book1, user=self.usr, review_text='Book1 review1',rating=1)
        b1r2 = BookReview.objects.create(book=book1, user=usr2, review_text='Book1 review2',rating=5)
        b2r1 = BookReview.objects.create(book=book2, user=self.usr, review_text='Book2 review1',rating=2)
        b2r2 = BookReview.objects.create(book=book2, user=usr2, review_text='Book2 review2',rating=3)

        response = self.client.get(reverse("api:api-all_book_review"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data["count"],4)

        lst=[b2r2,b2r1,b1r2,b1r1]
        ind=0

        for review in response.data["results"]:
            br = lst[ind]
            self.assertEqual(review["id"], br.id)
            self.assertEqual(review["review_text"], br.review_text)
            self.assertEqual(review["rating"], br.rating)
            # review user
            self.assertEqual(review["user"]["id"], br.user.id)
            self.assertEqual(review["user"]["username"], br.user.username)
            self.assertEqual(review["user"]["first_name"], br.user.first_name)
            self.assertEqual(review["user"]["last_name"], br.user.last_name)
            self.assertEqual(review["user"]["email"], br.user.email)
            # review book
            self.assertEqual(review["book"]["id"], br.book.id)
            self.assertEqual(review["book"]["title"], br.book.title)
            self.assertEqual(review["book"]["isbn"], br.book.isbn)
            ind+=1

    def test_book_review_user_authenticated(self):
        notauthuser = User.objects.create_user(username='userbek2', email='test2@mail.com')
        notauthuser.set_password('testpassword123')
        notauthuser.save()

        book=Book.objects.create(title='Book1', isbn='121212121212',discription="Tez uxlash siri")
        response_all_review = self.client.get(reverse("api:api-all_book_review"))
        response_one_review = self.client.get(reverse("api:api-book_review", kwargs={'id':book.id}))

        self.assertEqual(response_all_review.status_code, 403)
        self.assertEqual(response_one_review.status_code, 403)

    def test_book_review_paginated(self):
        self.client.force_login(self.usr)
        book=Book.objects.create(title=f'Book', discription=f'Discription', isbn=f'1212121212')

        for i in range(17):
            BookReview.objects.create(review_text=f"RT{i}",rating=3,book=book,user=self.usr)


        response = self.client.get(reverse("api:api-all_book_review"))
        response2 = self.client.get(reverse("api:api-all_book_review")+"?page=2")



        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"],17)
        self.assertEqual(response2.data["count"],17)

        self.assertEqual(len(response.data["results"]), 10)
        self.assertEqual(len(response2.data["results"]), 7)

    def test_book_review_delete(self):
        self.client.force_login(self.usr)

        book=Book.objects.create(title=f'Book', discription=f'Discription', isbn=f'1212121212')
        br = BookReview.objects.create(review_text=f"RT", rating=3, book=book, user=self.usr)

        response = self.client.delete(reverse("api:api-book_review",kwargs={'id':br.id}))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(BookReview.objects.all().count(), 0)
        self.assertFalse(BookReview.objects.filter(id=br.id).exists())

    def test_book_review_update(self):
        self.client.force_login(self.usr)

        book=Book.objects.create(title=f'Book', discription=f'Discription', isbn=f'1212121212')
        br = BookReview.objects.create(review_text=f"RT", rating=3, book=book, user=self.usr)

        response = self.client.patch(reverse("api:api-book_review",kwargs={'id':br.id}),data={'rating':4,"review_text":"rrtt"})

        br.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(br.rating, 4)
        self.assertEqual(br.review_text, "rrtt")

    def test_book_review_create(self):
        self.client.force_login(self.usr)

        book=Book.objects.create(title=f'Book', discription=f'Discription', isbn=f'1212121212')

        response = self.client.post(reverse("api:api-all_book_review"),data={"rating":4,"review_text":"Bu test comment","book_id":book.id,"user_id":self.usr.id})
        r1=BookReview.objects.first()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(BookReview.objects.all().count(), 1)
        self.assertEqual(r1.review_text, "Bu test comment")
        self.assertEqual(r1.rating, 4)

















