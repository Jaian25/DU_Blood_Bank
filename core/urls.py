from django.contrib import admin
from django.urls import include, path
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', obtain_auth_token),
    path('users/', include('users.urls')),
    # path('agencies/', include('project.urls')),
    # path('components/', include('project.urls')),
    path('constraints/', include('constraint.urls')),
    path('projects/', include('project.urls')),
]
