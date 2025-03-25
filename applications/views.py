from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from .forms import ApplicantDataForm, FamilyDataForm
from django.shortcuts import render
from .models import Application, ApplicationHistory, ApplicationDocument
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

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

# def create_application(request):
#     return render(request, 'create_application.html')

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Application, ApplicationHistory
from .forms import ApplicantDataForm, FamilyDataForm, ApplicationSubmissionForm, save_application_with_documents

@login_required
def create_application(request):
    """View to create a new application"""
    # Check if user already has an application
    # existing_application = Application.objects.filter(applicant=request.user).first()
    
    if request.method == 'POST':
        applicant_form = ApplicantDataForm(request.POST)
        family_form = FamilyDataForm(request.POST, request.FILES)
        submission_form = ApplicationSubmissionForm(request.POST)
        
        if all([applicant_form.is_valid(), family_form.is_valid(), submission_form.is_valid()]):
            try:
                # Save all forms
                application = save_application_with_documents(
                    applicant_form, family_form, submission_form, request.user
                )
                
                # Create initial history record
                ApplicationHistory.objects.create(
                    application=application,
                    previous_status='',
                    new_status='SUBMITTED',
                    changed_by=request.user,
                    notes=submission_form.cleaned_data.get('notes', '')
                )
                
                messages.success(request, 'Application submitted successfully!')
                return redirect('applications:view-application', application_id=application.id or 1)
            
            except Exception as e:
                messages.error(request, f'Error submitting application: {str(e)}')
        else:
            # Forms have errors
            messages.error(request, 'Please correct the errors in the form.')
    else:
        # Initialize forms
        initial_data = {}
        # if existing_application:
        #     # Prefill form with existing data
        #     initial_data = {
        #         field: getattr(existing_application, field)
        #         for field in ApplicantDataForm.Meta.fields + FamilyDataForm.Meta.fields
        #         if hasattr(existing_application, field)
        #     }
            
        applicant_form = ApplicantDataForm(initial=initial_data)
        family_form = FamilyDataForm(initial=initial_data)
        submission_form = ApplicationSubmissionForm()
    
    context = {
        'applicant_form': applicant_form,
        'family_form': family_form,
        'submission_form': submission_form,
        # 'existing_application': existing_application,
    }
    
    return render(request, 'create_application.html', context)

@login_required
def get_application_data(request):
    """View to display application details"""
    application = Application.objects.filter(applicant=request.user)
    
    if not application:
        messages.info(request, 'You have not submitted an application yet.')
        return redirect('create_application')
    
    # Get application history
    history = application.history.all().order_by('-change_date')
    
    # Get queue position if in queue
    queue_position = None
    if application.status == 'IN_QUEUE':
        higher_priority_count = Application.objects.filter(
            status='IN_QUEUE',
            priority_score__gt=application.priority_score
        ).count()
        queue_position = higher_priority_count + 1
    
    context = {
        'application': application,
        'history': history,
        'queue_position': queue_position,
    }
    
    return render(request, 'view_application.html', context)
@login_required
def view_application(request, application_id):
    application = get_object_or_404(Application, id=application_id, applicant=request.user)
    
    # Format application data for response
    application_data = {
        'id': application.id,
        'application_number': application.application_number,
        'status': application.get_status_display(),
        'priority_score': application.priority_score,
        'submission_date': application.submission_date.strftime('%Y-%m-%d %H:%M'),
        'applicant': application.applicant,
        'monthly_income': application.monthly_income,
        'children_count': application.children_count,
        'has_disability': application.has_disability,
        'current_living_area': application.current_living_area,
        'adults_count': application.adults_count,
        'elderly_count': application.elderly_count,
        'is_veteran': application.is_veteran,
        'is_single_parent': application.is_single_parent,
        'waiting_years': application.waiting_years,
        'document_verified': application.document_verified,
        'documents': [doc.file.url for doc in application.documents.all()],
    }

    # Get history data
    history_data = []
    for history in application.history.all().order_by('-change_date'):
        history_data.append({
            'date': history.change_date.strftime('%Y-%m-%d %H:%M'),
            'previous_status': history.get_previous_status_display(),
            'new_status': history.get_new_status_display(),
            'changed_by': history.changed_by.get_full_name() if history.changed_by else 'System',
            'notes': history.notes,
        })
    
    return render(request, 'view_application.html', {
        'success': True,
        'application': application_data,
        'history': history_data,
    })
