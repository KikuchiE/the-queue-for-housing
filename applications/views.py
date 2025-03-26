from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .forms import ApplicantDataForm, FamilyDataForm
from django.shortcuts import render
from .models import Application, ApplicationHistory, ApplicationDocument
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages
from users.models import User
from .forms import ApplicantDataForm, FamilyDataForm, ApplicationSubmissionForm, QueueCheckForm, QueueSearchForm,save_application_with_documents
from django.db.models import Window, F
from django.db.models.functions import RowNumber


# Create your views here.
def home(request):
    return render(request, 'info.html')

def statistics(request):
    return render(request, 'statistics.html')

def check_queue_number(request):
    if request.method == 'POST':
        form = QueueCheckForm(request.POST)
        if form.is_valid():
            iin = form.cleaned_data['iin']
            
            try:
                # Find the user with the given IIN
                user = User.objects.get(iin=iin)
                
                # Find all applications for this user
                applications = Application.objects.filter(
                    applicant=user, 
                    status__in=['SUBMITTED', 'UNDER_REVIEW', 'IN_QUEUE']
                ).order_by('submission_date')
                
                if applications.exists():
                    # Get all applications in the same statuses, ordered by priority score
                    all_queued_applications = Application.objects.filter(
                        status__in=['SUBMITTED', 'UNDER_REVIEW', 'IN_QUEUE']
                    ).order_by('-priority_score', 'submission_date')
                    
                    # Calculate queue position
                    queue_position = list(all_queued_applications).index(applications.first()) + 1
                    
                    context = {
                        'form': form,
                        'applications': applications,
                        'queue_position': queue_position,
                        'total_queued_applications': all_queued_applications.count()
                    }
                    return render(request, 'queue_check_result.html', context)
                else:
                    messages.warning(request, 'No active applications found for this IIN.')
                    return render(request, 'check_queue.html', {'form': form})
            
            except User.DoesNotExist:
                messages.error(request, 'No user found with this IIN.')
                return render(request, 'check_queue.html', {'form': form})
    
    else:
        form = QueueCheckForm()
    
    return render(request, 'check_queue.html', {'form': form})

def my_applications(request):
    applications = Application.objects.filter(applicant=request.user).order_by('-submission_date')
    
    # Pagination
    paginator = Paginator(applications, 10)  # Show 10 applications per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'my_applications.html', {
        'applications': page_obj,
        'applications_count': paginator.count,
    })

@login_required
def create_application(request):
    """View to create a new application"""
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
        applicant_form = ApplicantDataForm()
        family_form = FamilyDataForm()
        submission_form = ApplicationSubmissionForm()
    
    context = {
        'applicant_form': applicant_form,
        'family_form': family_form,
        'submission_form': submission_form,
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
        'is_for_ward': application.is_for_ward,
        'application_number': application.application_number,
        'status': application.get_status_display(),
        'priority_score': application.priority_score,
        'submission_date': application.submission_date.strftime('%Y-%m-%d %H:%M'),
        'applicant': application.applicant,
        'monthly_income': application.monthly_income,
        'children_count': application.children_count,
        'has_disability': application.has_disability,
        'current_address': application.current_address,
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

def queue_members(request):
    # Initialize the search form
    form = QueueSearchForm(request.GET or None)
    
    # Annotate queue number based on priority score ranking
    queryset = Application.objects.filter(status='SUBMITTED').annotate(
        queue_number=Window(
            expression=RowNumber(),
            order_by=F('priority_score').desc()
        )
    ).order_by('-priority_score')
    
    # Apply form filters if the form is valid
    if form.is_valid():
        iin = form.cleaned_data.get('iin')
        queue_number_from = form.cleaned_data.get('queue_number_from')
        queue_number_to = form.cleaned_data.get('queue_number_to')
        
        # Filter by IIN if provided
        if iin:
            queryset = queryset.filter(applicant__iin__icontains=iin)
        
        # Filter by queue number range if both from and to are provided
        if queue_number_from is not None and queue_number_to is not None:
            queryset = queryset.filter(
                queue_number__gte=queue_number_from,
                queue_number__lte=queue_number_to
            )
    
    # Pagination
    page = request.GET.get('page', 1)
    paginator = Paginator(queryset, 10)  # 10 items per page
    
    try:
        queue_members = paginator.page(page)
    except PageNotAnInteger:
        queue_members = paginator.page(1)
    except EmptyPage:
        queue_members = paginator.page(paginator.num_pages)
    
    context = {
        'form': form,
        'queue_members': queue_members,
    }
    
    return render(request, 'queue_members.html', context)
