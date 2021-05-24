from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from validate_email import validate_email
from django.contrib.auth.forms import PasswordResetForm

from .models import *

class CreateUserForm(UserCreationForm):
	class Meta:
		model = User
		fields = ['username', 'email', 'password1', 'password2']

	def clean_email(self):
		email = self.cleaned_data.get('email')

		if self.isEmailValid(email):
			try:
				match = User.objects.get(email = email)
			except User.DoesNotExist:
				return email
			raise forms.ValidationError('This email address is already in use.')
		else:
			raise forms.ValidationError('This email address is Invalid.')

	def isEmailValid(self,email):
		try:
			validate_email(email,check_mx=True,verify=True)
			return True
		except :
			return False

class EmailValidationOnForgotPassword(PasswordResetForm):
	def clean_email(self):
		email = self.cleaned_data['email']
		try:
			match = User.objects.get(email = email)
			return email
		except User.DoesNotExist:
			raise forms.ValidationError('There is no user registered with the specified E-Mail address.')
