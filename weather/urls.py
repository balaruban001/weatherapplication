from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("compare/", views.compare, name="compare"),
    path("current/", views.current_location, name="current_location"),
]
