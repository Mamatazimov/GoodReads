from django.core.mail import send_mail

from manage.celery import app


@app.task()
def send_email(subject,message,recipient_list):
    send_mail(subject,message,"jaloliddin6003@gmail.com",recipient_list)