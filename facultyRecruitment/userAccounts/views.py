from django.shortcuts import render, redirect
from django.http import HttpResponse

from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import *
from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserForm
from django.contrib.auth.models import Group
# Create your views here.

# User can signIn with the username and password
def signIn(request):

	if request.method == 'POST':
		username = request.POST.get('username')
		password =request.POST.get('password')

		user = authenticate(request, username=username, password=password)

		if user is not None:
			login(request, user)
			return redirect('dashboard')
		else:
			messages.info(request, 'Username OR Password is incorrect.')

	context = {}
	return render(request, 'userAccounts/signIn.html', context)

def signOut(request):
	logout(request)
	return redirect('dashboard')

def signUp(request):

	form = CreateUserForm()
	if request.method == 'POST':
		form = CreateUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			username = form.cleaned_data.get('username')
			group = Group.objects.get(name = 'candidates')
			user.groups.add(group)

			messages.success(request, 'Account was created for ' + username)

			return redirect('login')

	context = {'form':form}
	return render(request, 'userAccounts/signUp.html', context)


def dashboard(request):
    return render(request,'jobs/dashboard.html')
