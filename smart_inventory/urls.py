from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', views.home, name='home'),
    path('users/', include('users.urls'), name='users'),
    path('inventory/', include('inventory.urls'), name='inventory'),

]
