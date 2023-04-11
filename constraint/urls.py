from django.urls import path
from .views import ConstraintAPI
urlpatterns = [

    path('',ConstraintAPI.as_view()),
    path('<int:pk>/', ConstraintAPI.as_view()),
]