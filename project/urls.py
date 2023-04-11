from django.urls import path
from .views import ProjectAPI, AgencyAPI, ComponentAPI,LocationAPI, ExectionIntervalAPI, load_data

urlpatterns = [

    path('',ProjectAPI.as_view()),
    path('<int:pk>/', ProjectAPI.as_view()),

    path('agencies/', AgencyAPI.as_view()),
    path('agencies/<int:pk>/', AgencyAPI.as_view()),

    path('components/', ComponentAPI.as_view()),
    path('components/<int:pk>/', ComponentAPI.as_view()),

    path('locations/', LocationAPI.as_view()),
    path('locations/<int:pk>/', LocationAPI.as_view()),

    path('executionIntervals/', ExectionIntervalAPI.as_view()),
    path('executionIntervals/<int:pk>/', ExectionIntervalAPI.as_view()),

    path('load-data/', load_data),    
    # path('', ProjectAPI.as_view()),
    # path('<int:pk>/', ProjectAPI.as_view())
]
