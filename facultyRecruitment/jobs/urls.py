from django.urls import path
from . import views



urlpatterns = [
	path('addJob/', views.addJob, name="addJob"),
	path('applyJob/', views.applyJob, name="applyJob"),
	path('jobDetails/', views.showJobDetails, name = "jobDetails"),
	path('dashboard/', views.dashboard, name = 'dashboard')
]
