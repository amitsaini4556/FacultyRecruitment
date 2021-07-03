from django.db import models
from django.db.models.base import Model
from django.db.models.deletion import CASCADE
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import User
from facultyRecruitment.validators import validatePhoneNumber

class CollegeImages(models.Model):
    CollegeId = models.AutoField(primary_key=True)
    collegeName = models.CharField(max_length=200)
    image = models.ImageField(upload_to=settings.MEDIA_ROOT)

    def __str__(self):
        return str(self.CollegeId)

class Jobs(models.Model):
    jobId = models.AutoField(primary_key=True)
    adminId = models.ForeignKey(User, on_delete=models.CASCADE)
    collegeId = models.ForeignKey(CollegeImages,on_delete=models.CASCADE)
    position = models.CharField(max_length=40)
    location = models.CharField(max_length=200,default='Udaipur (raj)')
    applyBy = models.DateField(timezone.now().strftime("%Y-%m-%d"))
    datePosted = models.DateTimeField(default=timezone.now)
    description = models.TextField()
    availablePositions = models.IntegerField()
    adminPhoneNumber = models.CharField(max_length=10)
    adminEmail = models.EmailField()
    collegeWebsite = models.URLField(max_length=200)
    class Meta:
        ordering = ['applyBy','-datePosted']
    def __str__(self):
        return str(self.jobId)

class Applicants(models.Model):
    userId = models.ForeignKey(User, on_delete=models.CASCADE)
    jobId = models.ForeignKey(Jobs, on_delete=models.CASCADE)
    status = models.CharField(max_length=50, default='In-Progress')
    name = models.CharField(max_length=40)
    email= models.EmailField(max_length=40)
    phoneNumber = models.CharField(max_length=13)
    location = models.TextField(max_length=100)
    resume = models.FileField()
    #cv = models.FileField()
    linkedInProfileLink = models.URLField(max_length=200)
    portfolioLink = models.URLField(max_length=200)
    queAboutUs = models.TextField()
    applyDate = models.DateField(default = timezone.now().strftime("%Y-%m-%d"))

    class Meta:
        unique_together = (('userId', 'jobId'),)

    def __str__(self):
        return str(self.name) + str(self.userId)

class Reminder(models.Model):
    userId = models.ForeignKey(User, on_delete=models.CASCADE)
    jobId = models.ForeignKey(Jobs, on_delete=models.CASCADE)

    class Meta:
        unique_together = (('userId', 'jobId'),)
    def __str__(self):
        return str(self.userId) + str(self.jobId)
