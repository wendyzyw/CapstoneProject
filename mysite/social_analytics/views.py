from django.shortcuts import render
from .forms import LoginForm,ChangepassForm,EdituserinfoForm
from django.contrib import auth
from django.http import HttpResponse
from  .models import UserInfo

# Create your views here.
def index(request):
	return render(request, 'index.html')
	
def login(request):
	if request.method =="POST":
		uf = LoginForm(request.POST)
		if uf.is_valid():
			username = request.POST.get('username', '')
			password = request.POST.get('password', '')
			user = auth.authenticate(username=username, password=password)
			if user is not None and user.is_active:
				request.session['username'] = user.username
				request.session['password'] = user.password
				request.session['first_name'] = user.first_name
				request.session['last_name'] = user.last_name
				request.session['email'] = user.email
				request.session['phone'] = user.phone
				request.session['city'] = user.city
				request.session['zip_code'] = user.zip_code
				request.session['address'] = user.address
				return render(request,'account-home.html')
			else:
				return render(request,'Login.html',{'uf':uf})
	else:
		uf=LoginForm()
		return render(request, 'Login.html',{'uf':uf})
	
# def dataview(request):
	# return render(request, 'DataView.html')

def account(request):
	return render(request, 'account-home.html')
	
def manage1(request):
	if request.method =="POST":
		uf = ChangepassForm(request.POST)
		if uf.is_valid():
			username=request.session.get('username')
			old_password = request.POST.get('old_password', '')
			user = auth.authenticate(username=username, password=old_password)
			if user is not None and user.is_active:
				new_password1 = request.POST.get('new_password1', '')
				new_password2=request.POST.get('new_password2','')
				if new_password1!=new_password2:
					return render(request,'Manage1_privacy.html',{'uf':uf,'message':'The new passwords entered are inconsistent!'})
				else:
					user.set_password(new_password1)
					user.save()
					return render(request,'Manage1_privacy.html',{'uf':uf,'message':'success!'})
			else:
				return render(request,'Manage1_privacy.html',{'uf':uf,'message':'Your old password is not correct!'})
		else:
			return render(request, 'Manage1_privacy.html', {'uf': uf, 'message': 'Please fill in all the information!'})
	else:
		uf=ChangepassForm()
		return render(request, 'Manage1_privacy.html',{'uf':uf})

def manage2(request):
	if request.method =="POST":
		uf = EdituserinfoForm(request.POST)
		if uf.is_valid():
			first_name = request.POST.get('first_name', '')
			last_name=request.POST.get('last_name','')
			address = request.POST.get('address', '')
			phone = request.POST.get('phone', '')
			zip_code = request.POST.get('zip_code', '')
			gender = request.POST.get('gender', '')
			state = request.POST.get('state', '')
			city = request.POST.get('city', '')
			username = request.session.get('username')
			UserInfo.objects.filter(username=username).update(first_name=first_name,last_name=last_name,address=address,phone=phone,zip_code=zip_code,gender=gender,
															   state=state,city=city)
			user = UserInfo.objects.get(username=username)
			request.session['username'] = user.username
			request.session['first_name'] = user.first_name
			request.session['last_name'] = user.last_name
			request.session['phone'] = user.phone
			request.session['city'] = user.city
			request.session['zip_code'] = user.zip_code
			request.session['address'] = user.address
			return render(request, 'Manage2_Personal.html', {'uf': uf, 'message': 'success!'})

		else:
			return render(request, 'Manage2_Personal.html', {'uf': uf, 'message': 'Please fill in all your information!'})
	else:
		uf=EdituserinfoForm()
		return render(request, 'Manage2_Personal.html',{'uf':uf})

def manage3(request):
	return render(request, 'Manage3_social.html')
	
def data(request):
	return render(request, 'data.html')
