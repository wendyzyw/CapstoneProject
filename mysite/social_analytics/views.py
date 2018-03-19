from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
def index(request):
	return render(request, 'index.html')
	
def login(request):
	return render(request, 'Login.html')
	
def dataview(request):
	return render(request, 'DataView.html')

def account(request):
	return render(request, 'Account.html')
	
def manage1(request):
	return render(request, 'Manage1_privacy.html')

def manage2(request):
	return render(request, 'Manage2_Personal.html')

def manage3(request):
	return render(request, 'Manage3_social.html')
