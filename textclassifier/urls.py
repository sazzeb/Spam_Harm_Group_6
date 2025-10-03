from django.contrib import admin
from django.urls import path
from spamham import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.home, name="home"),
    path("classify/", views.classify, name="classify"),
]
