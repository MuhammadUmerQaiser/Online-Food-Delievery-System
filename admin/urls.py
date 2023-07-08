from django.urls import path
from . import views


urlpatterns = [
    path('', views.authenticated_only(views.indexAdmin), name="indexAdmin"),
]