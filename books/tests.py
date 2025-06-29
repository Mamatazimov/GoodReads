from http.client import responses

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from books.models import Book, BookReview, Author, BookAuthor


class BooksTestCase(TestCase):
    def test_no_books(self):
        response = self.client.get(reverse('books:book_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No books available.")

    def test_book_list(self):
        book1=Book.objects.create(title='Book1',discription='Discription1',isbn='121212121212')
        book2=Book.objects.create(title='Book2',discription='Discription2',isbn='343434343434')
        book3=Book.objects.create(title='Book3',discription='Discription3',isbn='565656565656')
        response = self.client.get(reverse('books:book_list'))
        self.assertEqual(response.status_code, 200)

        books = Book.objects.all()

        for book in [book1,book2]:
            self.assertContains(response, book.title)

        response = self.client.get(reverse('books:book_list')+"?page=2")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, book3.title)
    
    def test_book_detail(self):
        book = Book.objects.create(title='Book3',discription='Discription3',isbn='565656565656')
        author = Author.objects.create(first_name='Aftorbek', last_name='Aftorbekov')
        BookAuthor.objects.create(author=author, book=book)
        user = User.objects.create(username='userbek',email='test@mail.com',first_name='Userjon',last_name='Usertoyev')
        user.set_password('<PASSWORD>')
        user.save()

        self.client.force_login(user)
        response = self.client.get(reverse('books:book_detail',kwargs={'id':book.id}))

        self.assertEqual(response.status_code,200)
        self.assertContains(response, book.discription)
        self.assertContains(response, book.title)

        self.assertContains(response, author.first_name)
        self.assertContains(response, author.last_name)


    def test_search_book(self):
        book1 = Book.objects.create(title='Bookbek', discription='Discription1', isbn='121212121212')
        book2 = Book.objects.create(title='Bookoy', discription='Discription2', isbn='343434343434')
        book3 = Book.objects.create(title='Bookjon', discription='Discription3', isbn='565656565656')

        response = self.client.get(reverse('books:book_list')+"?q=Bookbek")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, book1.title)
        self.assertNotContains(response, book2.title)
        self.assertNotContains(response, book3.title)

        response = self.client.get(reverse('books:book_list')+"?q=Bookoy")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, book2.title)
        self.assertNotContains(response, book1.title)
        self.assertNotContains(response, book3.title)

        response = self.client.get(reverse('books:book_list')+"?q=bookjon")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, book3.title)
        self.assertNotContains(response, book2.title)
        self.assertNotContains(response, book1.title)

class BookReviewTestCase(TestCase):
    def test_book_review(self):
        book1=Book.objects.create(title='Book1',discription='Discription1',isbn='121212121212')
        user = User.objects.create(username='userbek',email='test@mail.com',first_name='Userjon',last_name='Usertoyev')
        user.set_password('<PASSWORD>')
        user.save()

        self.client.force_login(user)

        self.client.post(reverse('books:book_detail',kwargs={'id':book1.id}),data={'review_text':"Nice book",'rating':4})

        bookreview=book1.bookreview_set.first()
        self.assertEqual(bookreview.review_text,"Nice book")
        self.assertEqual(bookreview.rating,4)
        self.assertEqual(bookreview.user,user)
        self.assertEqual(bookreview.book,book1)

    def test_stars_count(self):
        book1=Book.objects.create(title='Book1',discription='Discription1',isbn='121212121212')
        user = User.objects.create(username='userbek',email='test@mail.com',first_name='Userjon',last_name='Usertoyev')
        user.set_password('<PASSWORD>')
        user.save()

        self.client.force_login(user)

        response = self.client.post(reverse('books:book_detail',kwargs={'id':book1.id}),data={'review_text':"Nice book",'rating':7})

        book_review=book1.bookreview_set.all()

        self.assertNotEqual(response.status_code,302)
        self.assertEqual(book_review.count(),0)

    def test_home_page_review(self):
        book1=Book.objects.create(title='Book1',discription='Discription1',isbn='121212121212')
        user = User.objects.create(username='userbek',email='test@mail.com',first_name='Userjon',last_name='Usertoyev')
        user.set_password('<PASSWORD>')
        user.save()

        self.client.force_login(user)
        r1=BookReview.objects.create(book=book1,user=user,review_text='Nice bookbek',rating=4)
        r2=BookReview.objects.create(book=book1,user=user,review_text='Nice bookoy',rating=3)
        r3=BookReview.objects.create(book=book1,user=user,review_text='Nice bookjon',rating=1)

        response = self.client.get(reverse('home')+"?page_size=2")
        self.assertContains(response,r2.review_text)
        self.assertContains(response,r3.review_text)
        self.assertNotContains(response,r1.review_text)

    def test_edit_review(self):
        book1 = Book.objects.create(title='Book1', discription='Discription1', isbn='121212121212')
        user = User.objects.create(username='userbek', email='test@mail.com', first_name='Userjon',
                                   last_name='Usertoyev')
        user.set_password('<PASSWORD>')
        user.save()

        self.client.force_login(user)
        r1 = BookReview.objects.create(book=book1, user=user, review_text='Nice bookbek', rating=4)


        response = self.client.post(reverse("books:book_update",kwargs={'rid':r1.id,'bid':book1.id}),data={'review_text':'Good bookbek ishonuvir','rating':5})
        r1.refresh_from_db()
        self.assertNotEqual('Nice bookbek',r1.review_text)
        self.assertEqual('Good bookbek ishonuvir',r1.review_text)
        self.assertEqual(r1.rating,5)

    def test_delete_review(self):
        book1 = Book.objects.create(title='Book1', discription='Discription1', isbn='121212121212')
        user = User.objects.create(username='userbek', email='test@mail.com', first_name='Userjon',
                                   last_name='Usertoyev')
        user.set_password('<PASSWORD>')
        user.save()

        self.client.force_login(user)
        r1 = BookReview.objects.create(book=book1, user=user, review_text='Nice bookbek', rating=4)

        response = self.client.post(reverse("books:book_delete",kwargs={'rid':r1.id,'bid':book1.id}))

        self.assertEqual(BookReview.objects.count(),0)
        self.assertFalse(BookReview.objects.filter(pk=r1.id).exists())


class BookAuthorTestCase(TestCase):
    def test_book_author(self):
        book = Book.objects.create(title='Book1', discription='Discription1', isbn='121212121212')
        user = User.objects.create(username='userbek', email='test@mail.com', first_name='Userjon',
                                   last_name='Usertoyev')
        user.set_password('<PASSWORD>')
        user.save()

        self.client.force_login(user)

        author = Author.objects.create(first_name="fn_author",last_name="ln_author",email="menauthor@mail.com",bio="Bu author bizning djangoni test casei uchun oylab topilgan.")
        BookAuthor.objects.create(book=book,author=author)

        response = self.client.get(reverse("books:book_author",kwargs={"id":book.id}))

        self.assertEqual(response.status_code,200)
        self.assertContains(response,author.first_name)
        self.assertContains(response,author.last_name)
        self.assertContains(response,author.email)
        self.assertContains(response,author.bio)

    def test_limit_book_author(self):
        author = Author.objects.create(first_name="fn_author",last_name="ln_author",email="menauthor@mail.com",bio="Bu author bizning djangoni test casei uchun oylab topilgan.")
        user = User.objects.create(username='userbek', email='test@mail.com', first_name='Userjon',
                                           last_name='Usertoyev')
        user.set_password('<PASSWORD>')
        user.save()

        self.client.force_login(user)

        for i in range(13):
            book = Book.objects.create(title=f'Book{i}', discription='Discription1', isbn=f'{i}121212121212')
            BookAuthor.objects.create(book=book,author=author)



        response = self.client.get(reverse("books:book_author",kwargs={"id":author.id}))

        self.assertEqual(response.status_code,200)
        self.assertContains(response,"Book1")
        self.assertContains(response,"Book5")
        self.assertContains(response,"Book9")
        self.assertNotContains(response,"Book10")
        self.assertNotContains(response,"Book12")













    