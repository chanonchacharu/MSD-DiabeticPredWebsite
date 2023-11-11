from django.shortcuts import render

def homepage(request):
    return render(request, "components/homepage.html")


def test(request):
    return render(request, "components/header.html")