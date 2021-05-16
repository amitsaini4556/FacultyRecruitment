from typing_extensions import Required
from django.db import models
from django.db.models.base import Model
from django.db.models.deletion import CASCADE
from facultyRecruitment.facultyRecruitment.settings import DATE_INPUT_FORMATS
from django.utils import timezone
from django.contrib.auth.models import User
from facultyRecruitment.validators import validatePhoneNumber
from facultyRecruitment.jobs.utils import COLLEGES, STATUS

class Jobs(models.Model):
    jobId = models.AutoField(primary_key=True)
    adminId = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    position = models.CharField(max_length=40)
    applyBy = models.DateField(input_formats=DATE_INPUT_FORMATS)
    datePosted = models.DateTimeField(default=timezone.now)
    description = models.TextField()
    collegeName = models.CharField(max_length=50, choices=COLLEGES)
    availablePositions = models.IntegerField()
    image = models.ImageField()
    adminPhoneNumber = models.CharField(validators=[validatePhoneNumber], max_length=10)
    adminEmail = models.EmailField()
    collegeWebsite = models.URLField(max_length=200)

    def __str__(self):
        return str(self.jobId) + " " + str(self.adminId) + " " + str(self.title) + " " + str(self.position) + " " + str(self.datePosted) + " " + str(self.applyBy) + " " + str(self.collegeName) + " " + str(self.availablePositions)

class Applicants(models.Model):
    userId = models.ForeignKey(User, on_delete=models.CASCADE)
    jobId = models.ForeignKey(Jobs, on_delete=models.CASCADE)
    status = models.CharField(max_length=50, choices=STATUS, default='inProgress')
    name = models.CharField(max_length=40)
    email= models.EmailField(max_length=40)
    phoneNumber = models.CharField(validators=[validatePhoneNumber], max_length=10)
    location = models.TextField(max_length=100)
    resume = models.URLField(max_length=200)
    cv = models.URLField(max_length=200)
    linkedInProfileLink = models.URLField(max_length=200, Required=False)
    portfolioLink = models.URLField(max_length=200, Required=False)
    queAboutUs = models.TextField()

    class Meta:
        unique_together = (('userId', 'jobId'),)

    def __str__(self):
        return str(self.userId) + " " + str(self.jobId) + " " + str(self.status) + " " + str(self.name) + " " + str(self.email) + " " + str(self.phoneNumber) + " " + str(self.location)
