from django.shortcuts import render
from courses.models import Course

# Create your views here.


def home_page(request):
    # get list of created courses
    courses = Course.objects.all()
    context = {"courses": courses}
    return render(request, "pages/home_page.html", context)



def page_not_found(request, exception):
    return render(request, "pages/404.html")

def server_error(request):
    return render(request, "pages/500.html")