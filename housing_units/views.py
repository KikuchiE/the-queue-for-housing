from django.shortcuts import render
from .models import HousingUnit
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.core.paginator import Paginator

# Create your views here.

def housing_units_list(request):
    units = HousingUnit.objects.all()
    paginator = Paginator(units, 10)  # 10 units per page
    page_number = request.GET.get('page')
    housing_units = paginator.get_page(page_number)
    
    context = {
        'housing_units': housing_units,
        'housing_units_count': units.count()
    }
    return render(request, 'housing_units.html', context)

def create_housing_unit(request):
    if request.method == 'POST':
        form_data = request.POST
        try:
            unit = HousingUnit.objects.create(
                unit_number=form_data.get('unit_number'),
                address=form_data.get('address'),
                floor=form_data.get('floor'),
                total_area=form_data.get('total_area'),
                rooms_count=form_data.get('rooms_count'),
                status=form_data.get('status'),
                is_accessible=form_data.get('is_accessible') == 'on',
                has_elevator=form_data.get('has_elevator') == 'on',
                has_heating=form_data.get('has_heating') == 'on',
                next_available_date=form_data.get('next_available_date') or None
            )
            messages.success(request, 'Housing unit created successfully!')
            return redirect('housing_units:view-unit', unit.id)
        except Exception as e:
            messages.error(request, f'Error creating housing unit: {str(e)}')
    
    return render(request, 'create_housing_unit.html')

def view_housing_unit(request, unit_id):
    unit = get_object_or_404(HousingUnit, id=unit_id)
    context = {
        'unit': unit,
        'view_mode': 'view'
    }
    return render(request, 'view_housing_unit.html', context)

def edit_housing_unit(request, unit_id):
    unit = get_object_or_404(HousingUnit, id=unit_id)
    
    if request.method == 'POST':
        try:
            unit.unit_number = request.POST.get('unit_number')
            unit.address = request.POST.get('address')
            unit.floor = request.POST.get('floor')
            unit.total_area = request.POST.get('total_area')
            unit.rooms_count = request.POST.get('rooms_count')
            unit.status = request.POST.get('status')
            unit.is_accessible = request.POST.get('is_accessible') == 'on'
            unit.has_elevator = request.POST.get('has_elevator') == 'on'
            unit.has_heating = request.POST.get('has_heating') == 'on'
            unit.next_available_date = request.POST.get('next_available_date') or None
            
            unit.save()
            messages.success(request, 'Housing unit updated successfully!')
            return redirect('housing_units:view-unit', unit.id)
        except Exception as e:
            messages.error(request, f'Error updating housing unit: {str(e)}')
    
    context = {
        'unit': unit,
        'view_mode': 'edit'
    }
    return render(request, 'view_housing_unit.html', context)