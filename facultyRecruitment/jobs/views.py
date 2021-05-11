from django.shortcuts import render


def showAddJobForm(request):
    return render(request,'jobs/addJobForm.html')
