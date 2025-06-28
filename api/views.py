from rest_framework import status, generics, viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from api.serializers import ApiReviewSerializer
from books.models import BookReview,Book



# class BookReviewViewSet(viewsets.ModelViewSet): ModelViewSet bilan ham bajarib ko'rmoqchi edim urllarni nomi o'zgarib chalkashlikga olib keldi!
#     queryset = BookReview.objects.all().order_by('-created_at')
#     serializer_class = ApiReviewSerializer
#     pagination_class = PageNumberPagination
#     permission_classes = (IsAuthenticated,)


class ApiBookReviewView(APIView):#(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    # serializer_class = ApiReviewSerializer
    # queryset = BookReview.objects.all()
    # lookup_field = 'id'

    def get(self,request,id):
        review = BookReview.objects.get(id=id)
        serializer = ApiReviewSerializer(review)
        return Response(serializer.data)

    def delete(self,request,id):
        review = BookReview.objects.get(id=id)
        review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def patch(self,request,id):
        review = BookReview.objects.get(id=id)
        serializer = ApiReviewSerializer(instance=review, data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data,status=status.HTTP_200_OK)
        return Response(data=serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class ApiAllBookReviewView(APIView):#(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    # serializer_class = ApiReviewSerializer
    # queryset = BookReview.objects.all().order_by('-created_at')


    def get(self,request):
        books = BookReview.objects.all().order_by('-created_at')

        pagination=PageNumberPagination()
        page_obj = pagination.paginate_queryset(books, request)
        serializer = ApiReviewSerializer(page_obj, many=True)


        return pagination.get_paginated_response(serializer.data)

    def post(self,request):
        serializer = ApiReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data,status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors,status=status.HTTP_400_BAD_REQUEST)

