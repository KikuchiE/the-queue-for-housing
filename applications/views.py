from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, 'info.html')

def statistics(request):
    return render(request, 'statistics.html')

def check_queue(request):
    return render(request, 'check_queue.html')

def list_queue(request):
    return render(request, 'list_queue.html')

def my_applications(request):
    return render(request, 'my_applications.html')

def create_application(request):
    return render(request, 'create_application.html')