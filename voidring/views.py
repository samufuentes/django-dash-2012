from django.shortcuts import render_to_response

def home(request):
    return render_to_response('home.html')

def index(request):
    return render_to_response('index.html')
