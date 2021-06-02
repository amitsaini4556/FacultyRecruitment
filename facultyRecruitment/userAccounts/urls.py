from django.urls import path
from . import views
from userAccounts.forms import EmailValidationOnForgotPassword
from django.contrib.auth import views as auth_views



urlpatterns = [
	path('login/', views.signIn, name="login"),
	path('logout/', views.signOut, name="logout"),
	path('register/', views.signUp, name="register"),
	path('logout/', views.signOut, name="logout"),
	path('', views.jobs, name="jobs"),
	path('reset_password/',
        auth_views.PasswordResetView.as_view(form_class=EmailValidationOnForgotPassword,template_name="userAccounts/password_reset.html"),
        name='reset_password'),
    path('reset_password_sent/',
        auth_views.PasswordResetDoneView.as_view(template_name="userAccounts/password_reset_sent.html"),
        name="password_reset_done"),

    path('reset/<uidb64>/<token>/',
     auth_views.PasswordResetConfirmView.as_view(template_name="userAccounts/password_reset_form.html"),
     name="password_reset_confirm"),

    path('reset_password_complete/',
        auth_views.PasswordResetCompleteView.as_view(template_name="userAccounts/password_reset_done.html"),
        name="password_reset_complete")
]
