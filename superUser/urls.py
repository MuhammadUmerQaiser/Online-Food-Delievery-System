from django.urls import path
from . import views


urlpatterns = [
    path('', views.authenticated_only(views.indexAdmin), name="indexAdmin"),
    path('profile/', views.authenticated_only(views.adminProfile), name="adminProfile"),
    path('edit-profile/', views.authenticated_only(views.editProfile), name="editProfile"),
    path('category/', views.authenticated_only(views.adminCategory), name="adminCategory"),
    path('category/create/', views.authenticated_only(views.createCategory), name="createCategory"),
    path('category/delete/', views.authenticated_only(views.deleteCategory), name="deleteCategory"),
    path('food-type/', views.authenticated_only(views.adminFoodType), name="adminFoodType"),
    path('food-type/create/', views.authenticated_only(views.createFoodType), name="createFoodType"),
    path('food-type/delete/', views.authenticated_only(views.deleteFoodType), name="deleteFoodType"),
]