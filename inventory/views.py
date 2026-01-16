from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .decorators import group_required, multi_group_required

# @login_required
def products(req):
    return render(req, 'inventory/products.html')

# @login_required
def dashboard(req):
    return render(req, 'inventory/dashboard.html')

def add_product(req):
    return render(req, 'inventory/add-product.html')

def update_product(req):
    return render(req, 'inventory/update-product.html')


def categories(req):
    return render(req, 'inventory/categories.html')

def categories_tree(req):
    return render(req, 'inventory/categories-tree.html')

def add_category(req):
    return render(req, 'inventory/add-category.html')

