from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from main.views import HomePageView
from manage import settings

urlpatterns = [
    path("admin/", admin.site.urls),
    path("users/", include('users.urls')), 
    path("books/", include('books.urls')),
    path("", HomePageView.as_view(), name="home"),
    path('api-auth/', include('rest_framework.urls')),
    path('api/', include('api.urls')),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
