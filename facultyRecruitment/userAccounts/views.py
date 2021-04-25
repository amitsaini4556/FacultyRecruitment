from django.shortcuts import render, redirect
from django.http import HttpResponse

from django.contrib.auth import authenticate, login
from django.contrib import messages
from .models import *
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


def dashboard(request):
    return render(request,'userAccounts/dashboard.html')
