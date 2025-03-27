from django.shortcuts import render
from applications.models import Application
from .forms import ApplicationFilterForm
from django.core.paginator import Paginator

# Create your views here.
def dashboard(request):
    # Initialize the filter form
    filter_form = ApplicationFilterForm(request.GET or None)
    
    # Start with all applications
    applications = Application.objects.all().order_by('-priority_score')
    
    # Apply filters if form is valid
    if filter_form.is_valid():
        applicant_iin = filter_form.cleaned_data.get('applicant_iin')
        application_number = filter_form.cleaned_data.get('application_number')
        status = filter_form.cleaned_data.get('status')
        
        # Apply filters conditionally
        if applicant_iin:
            applications = applications.filter(applicant__iin__icontains=applicant_iin)
        
        if application_number:
            applications = applications.filter(application_number__icontains=application_number)
        
        if status:
            applications = applications.filter(status=status)
    
    # Pagination
    paginator = Paginator(applications, 10)  # Show 10 applications per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'applications': page_obj,
        'filter_form': filter_form
    }
    
    return render(request, 'dashboard2.html', context)