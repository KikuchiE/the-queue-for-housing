from django.shortcuts import render
from applications.models import Application

# Create your views here.
def dashboard(request):
    context = {
        "applications": Application.objects.all().order_by("-priority_score")
    }
    return render(request, "dashboard2.html", context)