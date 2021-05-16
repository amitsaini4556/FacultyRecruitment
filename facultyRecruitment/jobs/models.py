from typing_extensions import Required
from django.db import models
from django.db.models.base import Model
from django.db.models.deletion import CASCADE
from facultyRecruitment.facultyRecruitment.settings import DATE_INPUT_FORMATS
from django.utils import timezone
from django.contrib.auth.models import User

class Jobs(models.Model):
    jobId = models.CharField(primary_key=True, max_length=10)
    adminId = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    position = models.CharField(max_length=40)
    applyBy = models.DateField(input_formats=DATE_INPUT_FORMATS)
    datePosted = models.DateTimeField(default=timezone.now)
    description = models.TextField()
    collegeName = models.CharField(max_length=50)
    availablePositions = models.IntegerField()

    def __str__(self):
        return str(self.jobId) + " " + str(self.adminId) + " " + str(self.title) + " " + str(self.position) + " " + str(self.datePosted) + " " + str(self.applyBy) + " " + str(self.collegeName) + " " + str(self.availablePositions)

class Applicants(models.Model):
    STATUS = (
    ('inProgress', _('Application is in progress')),
    ('accepted', _('Accepted by admin to proceed for further round of interviews')),
    ('rejected', _('Rejected - does not fit well in the job profile, hence rejected')),
    )

    userId = models.ForeignKey(User, on_delete=models.CASCADE, unique=True)
    jobId = models.ForeignKey(Jobs, on_delete=models.CASCADE, unique=True)
    status = models.CharField(max_length=50, choices=STATUS, default='inProgress')
    name = models.CharField(max_length=40)
    email= models.CharField(max_length=40)
    phoneNumber = models.CharField(max_length=12)
    location = models.TextField(max_length=100)
    resume = models.URLField(max_length=200)
    cv = models.URLField(max_length=200)
    linkedInProfileLink = models.URLField(max_length=200, Required=False)
    portfolioLink = models.URLField(max_length=200, Required=False)
    queAboutUs = models.TextField()

    def __str__(self):
        return str(self.userId) + " " + str(self.jobId) + " " + str(self.status) + " " + str(self.name) + " " + str(self.email) + " " + str(self.phoneNumber) + " " + str(self.location)
