from django.shortcuts import render
from rest_framework import views, response, status
from .serializer import StudentSerializer
from .models import *
from transformers import pipeline, set_seed
from django.core.mail import send_mail
from django.conf import settings
# from celery import shared_task
from .tasks import send_welcome_email, trigger_n8n_webhook



generator = pipeline('text-generation', model='distilgpt2')
set_seed(42)

def generate_welcome_message(prompt):
    result = generator(prompt, max_length=50,
                    num_return_sequences=1,
                    temperature=0.7,
                    top_p=0.9,
                    truncation=True
                )
    return result[0]['generated_text']


class StudentRegisterView(views.APIView):
    
    def post(self, request):
        serializer = StudentSerializer(data=request.data)
        if serializer.is_valid():
            student = serializer.save()
            msg = f"Generate a short welcome message for a student named {student.first_name} who enrolled in the {student.course} course."

            welcome_message = generate_welcome_message(msg)
            print("welcome_message:", welcome_message)
            send_welcome_email.delay(student.id, welcome_message)
            print('__________________________________________________________________________________________________')
            try:
                trigger_n8n_webhook.delay(student.id)
            except Exception as e:
                print("er:", e)
            return response.Response(
                {
                    "status": "success",
                    "message": "Student registered successfully",
                    "welcome_message": welcome_message,
                    "data": serializer.data
                },
                status=status.HTTP_201_CREATED
            )
        return response.Response(
            {
                "status": "error",
                "errors": serializer.errors
            },
            status=status.HTTP_400_BAD_REQUEST
        )