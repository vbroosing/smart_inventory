from django.shortcuts import render

# Create your views here.
def signin(req):
    return render(req, 'signin.html')