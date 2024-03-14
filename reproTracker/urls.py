from django.contrib import admin
from django.urls import path,include
from reproTracker_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('reproTracker_app.urls')),
]
