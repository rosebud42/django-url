from django.contrib import admin
from django.urls import path,include
from . import views

app_name = 'index'

urlpatterns = [
    path("", views.main, name="main"),
    path("/success/<str:token>/", views.success_view, name="success_view")
]
