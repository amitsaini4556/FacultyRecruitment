from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from userAccounts.decorators import allowed_users, admin_only

@admin_only
def addJob(request):
    return render(request,'jobs/addJobForm.html')

@login_required(login_url='login')
def applyJob(request):
    return render(request,'jobs/jobApplyForm.html')

def showJobDetails(request):
    return render(request, 'jobs/jobDetails.html')

@login_required(login_url='login')
def dashboard(request):
    return render(request, 'jobs/jobStatus.html')