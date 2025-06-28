from django.core.paginator import Paginator
from django.shortcuts import render
from django.views import View

from books.models import Book, BookReview


class HomePageView(View):
    def get(self, request):
        reviews = BookReview.objects.all().order_by('-created_at')
        page = request.GET.get('page_size',10)
        paginator = Paginator(reviews, page)

        page_num = request.GET.get('page',1)
        page_obj = paginator.get_page(page_num)


        return render(request, 'home.html',{ 'page_obj':page_obj})

