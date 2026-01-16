from django.shortcuts import render, redirect

def home(req):


    if req.user.is_authenticated:
        return redirect('dashboard')

    else:

        return redirect('signin')