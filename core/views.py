from django.shortcuts import render

# Create your views here.


def page_not_found(request, exception):
    return render(request, "core/404.html", status=404)

def server_error(request):
    return render(request, "core/500.html", status=500)