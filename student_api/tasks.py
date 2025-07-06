from celery import shared_task
from .models import *
from django.core.mail import send_mail
from django.conf import settings
import requests

@shared_task
def send_welcome_email(student_id, welcome_message):
    try:
        student = Student.objects.get(id=student_id)
        subject = f"Welcome to {student.course}!"
        message = (
            f"Dear {student.first_name} {student.last_name},"
            f"Welcome to your {student.course} course!"
            f"{welcome_message}"
        )
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[student.email],
            fail_silently=False,
        )
    except Student.DoesNotExist:
        print(f"Student with id {student_id} not found")
    except Exception as e:
        print(f"Error sending email: {str(e)}")

@shared_task
def trigger_n8n_webhook(student_id):
    student = Student.objects.get(id=student_id)
    payload = {
        "first_name": student.first_name,
        "last_name": student.last_name,
        "email": student.email,
        "course": student.course,
    }

    try:
        requests.post(settings.N8N_WEBHOOK_URL, json=payload)
    except Exception as e:
        print(f"Webhook error: {e}")