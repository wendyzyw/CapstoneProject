from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
def index(request):
	return render(request, 'index.html')
	
def login(request):
	return render(request, 'Login.html')
	
def dataview(request):
	return render(request, 'DataView.html')
