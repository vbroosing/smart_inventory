from django.shortcuts import render

# Create your views here.
def products(req):
    return render(req, 'inventory/products.html')

def dashboard(req):
    
    return render(req, 'inventory/dashboard.html')