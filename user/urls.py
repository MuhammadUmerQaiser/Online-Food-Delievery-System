from django.urls import path
from . import views


urlpatterns = [
    path('', views.authenticated_only(views.indexUser), name="indexUser"),
    path('profile/', views.authenticated_only(views.userProfile), name="userProfile"),
    path('edit-profile/', views.authenticated_only(views.editUserProfile), name="editUserProfile"),
    path('dish/', views.authenticated_only(views.userDish), name="userDish"),
    path('dish/create/', views.authenticated_only(views.createUserDish), name="createUserDish"),
    path('dish/delete/', views.authenticated_only(views.deleteUserDish), name="deleteUserDish"),
    path('dish/edit/<int:id>/', views.authenticated_only(views.editUserDish), name="editUserDish"),
    path('dish/update/<int:id>/', views.authenticated_only(views.updateUserDish), name="updateUserDish"),
]