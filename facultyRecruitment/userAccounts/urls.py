from django.urls import path
from . import views



urlpatterns = [
	path('login/', views.signIn, name="login"),
	path('register/', views.signUp, name="register"),
	path('', views.dashboard, name="dashboard"),
]
