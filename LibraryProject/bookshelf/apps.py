from django.apps import AppConfig


<<<<<<<< HEAD:advanced-api-project/api/apps.py
class ApiConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "api"
========
class BookshelfConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "bookshelf"
>>>>>>>> be8ad6a (Fix: removed nested git repo from django_blog folder):django_blog/LibraryProject/bookshelf/apps.py
