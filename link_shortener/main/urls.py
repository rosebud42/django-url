from django.urls import path

from . import views

app_name = "main"

urlpatterns = [
    path("", views.main, name="main"),
    path("/<str:token>/", view=views.view_link, name="linkview"),
    path("/<str:token>/edit", view=views.editlink, name="editlink"),
    path("/showall", view=views.showall, name="showall"),
]