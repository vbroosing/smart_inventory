from django.urls import path
from . import views

urlpatterns = [
    path('signin/', views.signin, name='signin'),
    path('dashboard/', views.dashboard, name='dashboard')

]
