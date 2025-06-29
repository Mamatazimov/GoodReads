from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.views.generic import ListView, DetailView, UpdateView

from .forms import ReviewForm
from .models import Book, BookReview, Author, BookAuthor


# class BookListView(ListView):
#     queryset = Book.objects.all()
#     template_name = 'books.html'
#     context_object_name = 'books'
#     paginate_by = 2

class BookListView(View):
    def get(self,request):
        books=Book.objects.all().order_by('id')
        search_query=request.GET.get('q','')

        if search_query:
            books=books.filter(title__icontains=search_query)

        page = request.GET.get('page',1)
        paginator = Paginator(books, 3)
        page_obj = paginator.get_page(page)
        return render(request,'books.html',{'page_obj':page_obj,"search_query":search_query})


# class BookDetailView(DetailView):
#     model = Book
#     template_name = 'book_detail.html'
#     context_object_name = 'book'
#     pk_url_kwarg = 'id'


class BookDetailView(LoginRequiredMixin, View):
    def get(self,request,id):
        book = Book.objects.filter(id=id).first()
        form=ReviewForm()
        return render(request,'book_detail.html',{'book':book,"form":form})

    def post(self,request,id):
        book = Book.objects.filter(id=id).first()
        form=ReviewForm(data=request.POST)
        if form.is_valid():
            BookReview.objects.create(
                book=book,
                user=request.user,
                rating=form.cleaned_data['rating'],
                review_text=form.cleaned_data['review_text'],
            )
            return redirect(reverse("books:book_detail",kwargs={"id":book.id}))
        return render(request,'book_detail.html',{'book':book,"form":form})

class ReviewUpdateView(LoginRequiredMixin, View):
    def get(self,request,rid,bid):
        book=Book.objects.filter(id=bid).first()
        review=book.bookreview_set.get(id=rid)
        form=ReviewForm(instance=review)
        return render(request,"book-review_edit.html",{'review':review,"form":form,"book":book})

    def post(self,request,bid,rid):
        book=Book.objects.filter(id=bid).first()
        review=book.bookreview_set.get(id=rid)
        form=ReviewForm(data=request.POST,instance=review)
        if form.is_valid():
            form.save()
            return redirect(reverse("books:book_detail",kwargs={"id":book.id}))
        return render(request, "book-review_edit.html", {'review': review, "form": form, "book": book})


class DeleteReviewView(LoginRequiredMixin, View):
    def get(self,request,rid,bid):
        book = Book.objects.filter(id=bid).first()
        review = book.bookreview_set.get(id=rid)
        form = ReviewForm(instance=review)
        return render(request,"book-review_delete.html",{'review':review,"form":form,"book":book})

    def post(self,request,rid,bid):
        book = Book.objects.filter(id=bid).first()
        review = book.bookreview_set.get(id=rid)
        review.delete()
        return redirect(reverse("books:book_detail",kwargs={"id":book.id}))


class BookAuthorView(View):
    def get(self,request,id):
        author=Author.objects.filter(id=id).first()
        return render(request,"book_author.html",{"author":author})

