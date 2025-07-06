Pip install requirements.txt file

Create a .env file in the project and add EMAIL_HOST_USER, EMAIL_HOST_PASSWORD, N8N_WEBHOOK_URL 

run the commands
python manage.py makemigrations
python manage.py migrate

run the server
python manage.py runserver

endpoint
http://127.0.0.1:8000/api/student/register/

payload
{
  "first_name": "akshay",
  "last_name": "s",
  "email": "akshay@example.com",
  "course": "science"
}

note:
n8n webhook not working not completed facing some error 
