from django.urls import path
from .views import UsersAPI, CurrentUserAPI,DonationsAPI

urlpatterns = [
    path('', UsersAPI.as_view()),
    path('current-user', CurrentUserAPI.as_view()),
    path('<int:pk>/', UsersAPI.as_view()),
    path('donations/', DonationsAPI.as_view()),
    path('donations/<int:pk>/', DonationsAPI.as_view()),
    
]
