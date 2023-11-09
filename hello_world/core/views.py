from django.shortcuts import render

def index(request):
    context = {
        "title": "Django example",
    }
    return render(request, "index.html", context)

def homepage(request):
    return render(
        request, 
        'components/layout.html'
    )

def homepage_v1(request):
    return render(
        request,
        'homepage.html'
    )