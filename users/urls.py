from django.urls import path
from .views import UsersAPI, CurrentUserAPI,ReviewAPI

urlpatterns = [
    path('', UsersAPI.as_view()),
    path('current-user', CurrentUserAPI.as_view()),
    path('<int:pk>/', UsersAPI.as_view()),
    path('reviews/', ReviewAPI.as_view()),
    path('reviews/<int:pk>/', ReviewAPI.as_view()),
    
]
