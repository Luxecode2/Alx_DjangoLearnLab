from django.contrib import admin
from django.urls import include, path  
from book_store import views   # import views from your app
 # <-- include added here


urlpatterns = [
    path("books/", include("book_store.urls")),  # send all /books/ to book_store app
    path("", views.index, name="home"),
    path("admin/", admin.site.urls),
]

