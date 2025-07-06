from rest_framework import serializers
from .models import Student
import re


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['first_name', 'last_name', 'email', 'course']

        def validate_email(self, value):
            email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if not re.match(email_regex, value):
                raise serializers.ValidationError("Invalid email format")
        
            # Check email uniqueness
            if Student.objects.filter(email=value).exists():
                raise serializers.ValidationError("Email already registered")
            return value