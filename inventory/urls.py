from django.urls import path
from . import views

urlpatterns = [

    path('dashboard/', views.dashboard, name='dashboard'),

    # PRODUCTS
    path('products/', views.products, name='products'),
    path('add-product/', views.add_product, name='add-product'),
    path('update-product/', views.update_product, name='update-product'),

    # CATEGORIES
    path('categories/', views.categories, name='categories'),
    path('categories-tree/', views.categories_tree, name='categories-tree'),
    path('add-category/', views.add_category, name='add-category'),

]
