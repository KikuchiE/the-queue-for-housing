from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Notification
from django.shortcuts import get_object_or_404

@login_required
def notification_list(request):
    # Filter notifications for the user's applications
    notifications = Notification.objects.filter(application__applicant=request.user).order_by('-created_at')
    return render(request, 'notification_list.html', {'notifications': notifications})

@login_required
def notification_details(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id, application__applicant=request.user)
    # Mark as 'READ' when viewed
    if notification.status == 'UNREAD':
        notification.status = 'READ'
        notification.save()
    return render(request, 'notification_details.html', {'notification': notification})