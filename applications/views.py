from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from .forms import ApplicantDataForm, FamilyDataForm, HouseholdMemberForm, ApplicationSubmissionForm
import json
from django.shortcuts import render
from .models import Application, ApplicationHistory, ApplicationDocument, HouseholdMember, HouseholdDocument
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

@login_required
def create_application(request):
    # Initialize forms
    applicant_form = ApplicantDataForm(prefix='applicant')
    family_form = FamilyDataForm(prefix='family')
    household_form = HouseholdMemberForm(prefix='household')
    submission_form = ApplicationSubmissionForm(prefix='submission')
    
    if request.method == 'POST':
        applicant_form = ApplicantDataForm(request.POST, prefix='applicant')
        family_form = FamilyDataForm(request.POST, request.FILES, prefix='family')
        submission_form = ApplicationSubmissionForm(request.POST, prefix='submission')
        
        if applicant_form.is_valid() and family_form.is_valid() and submission_form.is_valid():
            # Save applicant data
            application = applicant_form.save(commit=False)
            application.applicant = request.user
            application.save()
            
            # Save family data
            family_instance = family_form.save(commit=False)
            # Copy fields from family form to application instance
            application.is_single_parent = family_instance.is_single_parent
            application.is_veteran = family_instance.is_veteran
            application.has_disability = family_instance.has_disability
            application.save()
            
            # Handle disability document (now handled in family_form.save())
            family_form.instance = application
            family_form.save()
            
            # Save submission data
            submission_instance = submission_form.save(commit=False)
            application.notes = submission_instance.notes
            application.save()
            
            # Create initial history record
            ApplicationHistory.objects.create(
                application=application,
                previous_status='SUBMITTED',
                new_status='SUBMITTED',
                changed_by=request.user
            )
            
            # Calculate priority score
            application.calculate_priority()
            
            return redirect('application_detail', pk=application.id)
    
    context = {
        'applicant_form': applicant_form,
        'family_form': family_form,
        'household_form': household_form,
        'submission_form': submission_form,
    }
    
    return render(request, 'create_application.html', context)

@login_required
@require_POST
def add_household_member(request):
    try:
        data = json.loads(request.body)
        application_id = data.get('application_id')
        application = get_object_or_404(Application, id=application_id, applicant=request.user)
        
        form = HouseholdMemberForm(data)
        if form.is_valid():
            member = form.save(application=application)
            
            # Return the new member data for the table
            return JsonResponse({
                'success': True,
                'member': {
                    'id': member.id,
                    'full_name': member.full_name,
                    'date_of_birth': member.date_of_birth.strftime('%Y-%m-%d'),
                    'relationship': member.get_relationship_display(),
                    'has_disability': member.has_disability,
                }
            })
        else:
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=500)

@login_required
def get_application_data(request, application_id):
    application = get_object_or_404(Application, id=application_id, applicant=request.user)
    household_members = application.household_members.all()
    
    # Format application data for response
    application_data = {
        'id': application.id,
        'application_number': application.application_number,
        'status': application.get_status_display(),
        'priority_score': application.priority_score,
        'submission_date': application.submission_date.strftime('%Y-%m-%d %H:%M'),
    }
    
    # Format household members data
    members_data = []
    for member in household_members:
        members_data.append({
            'id': member.id,
            'full_name': member.full_name,
            'date_of_birth': member.date_of_birth.strftime('%Y-%m-%d'),
            'relationship': member.get_relationship_display(),
            'has_disability': member.has_disability,
        })
    
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
    
    return JsonResponse({
        'success': True,
        'application': application_data,
        'household_members': members_data,
        'history': history_data,
    })

@login_required
@csrf_protect
def submit_application(request):
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Only POST method is allowed'})
    
    try:
        # Create the main application
        application = Application(
            applicant=request.user,
            current_address=request.POST.get('current_address', ''),
            is_homeless=request.POST.get('is_homeless') == 'true',
            current_residence_condition=request.POST.get('current_residence_condition'),
            monthly_income=request.POST.get('monthly_income', 0),
            current_living_area=request.POST.get('current_living_area', None) or None,
            is_veteran=request.POST.get('is_veteran') == 'true',
            is_single_parent=request.POST.get('is_single_parent') == 'true',
            has_disability=request.POST.get('has_disability') == 'true',
            status='SUBMITTED'
        )
        application.save()
        
        # Process disability document if exists
        if request.FILES.get('applicant_disability'):
            disability_doc = ApplicationDocument(
                application=application,
                document_type='DISABILITY_CERTIFICATE',
                file=request.FILES['applicant_disability']
            )
            disability_doc.save()
        
        # Create application history
        ApplicationHistory.objects.create(
            application=application,
            previous_status='SUBMITTED',  # Initial status
            new_status='SUBMITTED',
            changed_by=request.user,
            notes=request.POST.get('notes', '')
        )
        
        # Process household members
        household_members = json.loads(request.POST.get('household_members', '[]'))
        member_files = json.loads(request.POST.get('member_files', '{}'))
        
        for idx, member_data in enumerate(household_members):
            # Create the household member
            household_member = HouseholdMember(
                application=application,
                full_name=member_data['name'],
                date_of_birth=member_data['birthdate'],
                relationship=member_data['relationship'],
                has_disability=member_data['hasDisability']
            )
            household_member.save()
            
            # Process member documents if they exist
            if str(idx) in member_files:
                files_data = member_files[str(idx)]
                
                # ID Document
                if 'id' in files_data and files_data['id'] in request.FILES:
                    id_doc = HouseholdDocument(
                        household_member=household_member,
                        document_type='ID_PROOF',
                        file=request.FILES[files_data['id']]
                    )
                    id_doc.save()
                
                # Disability Document
                if 'disability' in files_data and files_data['disability'] in request.FILES:
                    disability_doc = HouseholdDocument(
                        household_member=household_member,
                        document_type='DISABILITY_CERTIFICATE',
                        file=request.FILES[files_data['disability']]
                    )
                    disability_doc.save()
        
        # Calculate priority score
        application.calculate_priority()
        
        return JsonResponse({
            'success': True, 
            'application_number': application.application_number
        })
        
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})