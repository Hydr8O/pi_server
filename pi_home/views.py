from django.shortcuts import render

def home(request):
    return(render(
        request,
        'pi_home/home.html'
    ))
