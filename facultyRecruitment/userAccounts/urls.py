from django.urls import path
from . import views



urlpatterns = [
	path('login/', views.signIn, name="login"),
	path('logout/', views.signOut, name="logout"),
	path('register/', views.signUp, name="register"),
	path('logout/', views.signOut, name="logout"),
	path('', views.jobs, name="jobs"),
]
