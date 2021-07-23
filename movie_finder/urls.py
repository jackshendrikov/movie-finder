from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include("movies.urls")),
    path('', include("users.urls")),
    path('admin/', admin.site.urls),
]

handler403 = 'movies.views.error_403'
handler404 = 'movies.views.error_404'
handler500 = 'movies.views.error_500'
