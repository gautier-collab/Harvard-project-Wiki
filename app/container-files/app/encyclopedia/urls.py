from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("create", views.create, name="create"),
    path("redirect", views.redirect, name="redirect"),
    path("randomPage", views.randomPage, name="randomPage"),
    path("wiki/" + "<str:title>", views.entry, name="entry"),
    path("wiki/" + "<str:title>" + "/edit", views.edit, name="edit"),
]
