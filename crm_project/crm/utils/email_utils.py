from django.core.mail import send_mail
from django.conf import settings

def send_activity_email(to_email, activity_title, activity_type, due_date, created_by):
    subject = f"New {activity_type.capitalize()} Scheduled: {activity_title}"
    message = f"""
Hello,

A new {activity_type} has been scheduled for you.

Title: {activity_title}
Type: {activity_type.capitalize()}
Scheduled On: {due_date.strftime('%Y-%m-%d %H:%M')}
Created By: {created_by}

Please check your CRM dashboard for details.

Best regards,  
CRM System
"""
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [to_email],
        fail_silently=False,
    )