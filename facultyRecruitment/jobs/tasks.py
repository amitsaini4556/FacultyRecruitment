from . models import *
from django.contrib.auth.models import User
import datetime
from django.core.mail import BadHeaderError, send_mail
from django.template import Context
from django.template.loader import get_template
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

def myTask():
    remindlist = Reminder.objects.all()
    for remind in remindlist:
        if remind.jobId.applyBy == datetime.date.today() + datetime.timedelta(days = 1):
            #job = Jobs.objects.get(jobId = remind.jobId, applyBy = datetime.date.today() + datetime.timedelta(days = 1))
            toUserEmail = User.objects.only('email').get(id = remind.userId.id).email
            toUserName = User.objects.only('username').get(id = remind.userId.id).username

            html_template = 'jobs/reminder.html'
            context = {
                        'user': toUserName,
                        'job':remind.jobId
                        }
            html_message = render_to_string(html_template, context)
            subject = 'Reminder for job ' + remind.jobId.position
            message = EmailMessage(subject, html_message, 'tododjangowebapp@gmail.com', [toUserEmail])
            message.content_subtype = 'html'
            message.send()
