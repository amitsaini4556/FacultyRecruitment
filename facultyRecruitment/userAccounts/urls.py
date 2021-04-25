from django.urls import path
from . import views



urlpatterns = [
	path('login/', views.signIn, name="login"),
	path('', views.dashboard, name="dashboard"),
]
