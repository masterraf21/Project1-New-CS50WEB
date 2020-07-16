from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.show_entry, name="title"),
    path("wiki/", views.random_page, name="random"),
    path("new_page", views.new_page, name="new"),
]
