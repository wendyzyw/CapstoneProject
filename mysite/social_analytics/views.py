from django.shortcuts import render
from .forms import LoginForm, ChangepassForm, EdituserinfoForm, RegisterForm, MyPasswordResetForm
from django.contrib import auth
from django.http import HttpResponse
from .models import UserInfo
from django.contrib.auth.views import PasswordResetView, PasswordChangeView, \
    PasswordResetDoneView, PasswordChangeDoneView, PasswordResetConfirmView, PasswordResetCompleteView


# Create your views here.
def index(request):
    return render(request, 'index.html')


def login(request):
    if request.method == "POST":
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
                return render(request, 'account-home.html')
            else:
                return render(request, 'Login.html',
                              {'uf': uf, 'message': 'username or password is not correct, please check or signup!'})
        else:
            return render(request, 'Login.html', {'uf': uf,
                                                  'message': 'please fill in all the information or note the format of entered password!'})
    else:
        uf = LoginForm()
        return render(request, 'Login.html', {'uf': uf})

    # def dataview(request):
    # return render(request, 'DataView.html')


def account(request):
    return render(request, 'account-home.html')


def manage1(request):
    if request.method == "POST":
        uf = ChangepassForm(request.POST)
        if uf.is_valid():
            username = request.session.get('username')
            old_password = request.POST.get('old_password', '')
            user = auth.authenticate(username=username, password=old_password)
            if user is not None and user.is_active:
                new_password1 = request.POST.get('new_password1', '')
                if new_password1 == old_password:
                    return render(request, 'Manage1_privacy.html',
                                  {'uf': uf, 'message': 'Please set one different new password!'})
                else:
                    new_password2 = request.POST.get('new_password2', '')
                    if new_password1 != new_password2:
                        return render(request, 'Manage1_privacy.html',
                                      {'uf': uf, 'message': 'Please confirm your new password!'})
                    else:
                        user.set_password(new_password1)
                        user.save()
                        return render(request, 'Manage1_privacy.html', {'uf': uf, 'message': 'success!'})
            else:
                return render(request, 'Manage1_privacy.html',
                              {'uf': uf, 'message': 'Your old password is not correct!'})
        else:
            return render(request, 'Manage1_privacy.html', {'uf': uf, 'message':
                'Please fill in all the information or note the format of entered password (at least 8 characters, including both numbers and letters)!'})
    else:
        uf = ChangepassForm()
        return render(request, 'Manage1_privacy.html', {'uf': uf})


def manage2(request):
    if request.method == "POST":
        uf = EdituserinfoForm(request.POST)
        if uf.is_valid():
            first_name = request.POST.get('first_name', '')
            last_name = request.POST.get('last_name', '')
            address = request.POST.get('address', '')
            phone = request.POST.get('phone', '')
            zip_code = request.POST.get('zip_code', '')
            gender = request.POST.get('gender', '')
            state = request.POST.get('state', '')
            city = request.POST.get('city', '')
            username = request.session.get('username')
            UserInfo.objects.filter(username=username).update(first_name=first_name, last_name=last_name,
                                                              address=address, phone=phone, zip_code=zip_code,
                                                              gender=gender,
                                                              state=state, city=city)
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
            return render(request, 'Manage2_Personal.html',
                          {'uf': uf, 'message': 'Please fill in all your information!'})
    else:
        uf = EdituserinfoForm()
        return render(request, 'Manage2_Personal.html', {'uf': uf})


def manage3(request):
    return render(request, 'Manage3_social.html')


def data(request):
    return render(request, 'data.html')


def register(request):
    if request.method == 'POST':  # when submit the form
        uf = RegisterForm(request.POST)  # include the data submitted
        if uf.is_valid():  # if the data submitted is valid
            username = request.POST.get('username', '')
            first_name = request.POST.get('first_name', '')
            last_name = request.POST.get('last_name', '')
            email = request.POST.get('email', '')
            password = request.POST.get('password', '')
            password_confirm = request.POST.get('password_confirm', '')
            if password != password_confirm:
                return render(request, 'signup.html', {'uf': uf, 'message': 'please confirm your new password!'})
            else:
                try:
                    UserInfo.objects.create_user(username=username, password=password, email=email,
                                                 phone='0', first_name=first_name, last_name=last_name)
                    return login(request)
                except:
                    return render(request, 'signup.html', {'uf': uf, 'message': 'user has existed！'})
        else:
            return render(request, 'signup.html', {'uf': uf,
                                                   'message': 'Please fill in all information or note the format of entered password!'})
    else:
        uf = RegisterForm()
        return render(request, 'signup.html', {'uf': uf})


# Enter email address to reset password
class MyPasswordResetView(PasswordResetView):
    template_name = 'password_reset.html'
    form_class = MyPasswordResetForm


# Email Sent
class MyPasswordResetDone(PasswordResetDoneView):
    template_name = 'password_reset_done.html'


# Reset the password without requirement of the old password
class MyPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'password_reset_confirm.html'


# Password changed and go back to login
class MyPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'password_reset_complete.html'

    ####################################################
    # This two views below are for changing password with requirement of old password.
    ####################################################

    # class MyPasswordChangeView(PasswordChangeView):
    # template_name = 'password_change.html'

    # class MyPasswordChangeDoneView(PasswordChangeDoneView):
	# template_name = 'password_reset_complete.html'