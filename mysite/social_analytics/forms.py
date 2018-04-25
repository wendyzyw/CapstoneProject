from django import forms
from django.contrib.auth.forms import PasswordResetForm
from .models import UserInfo

pwd_min_length = 8


class LoginForm(forms.Form):
    username = forms.CharField(required=True, max_length=100)
    password = forms.CharField(required=True, max_length=100, min_length=pwd_min_length, widget=forms.PasswordInput())


class ChangepassForm(forms.Form):
    old_password = forms.CharField(
        required=True,
        label=u"old password",
        max_length=100,
        widget=forms.PasswordInput(),
    )
    new_password1 = forms.CharField(
        required=True,
        max_length=100,
        label=u"new password",
        min_length=pwd_min_length,
        widget=forms.PasswordInput(),
    )
    new_password2 = forms.CharField(
        required=True,
        max_length=100,
        label=u"confirm new password",
        min_length=pwd_min_length,
        widget=forms.PasswordInput(),
    )


class EdituserinfoForm(forms.Form):
    first_name = forms.CharField(required=True, max_length=100, label=u"first name")
    last_name = forms.CharField(required=True, max_length=100, label=u"last name")
    email = forms.EmailField(max_length=100, label=u"email")
    phone = forms.IntegerField(required=True, label=u"phone")
    address = forms.CharField(required=True, max_length=100, label=u"address")
    city = forms.CharField(required=True, max_length=100, label=u"city")
    gender = forms.CharField(required=True, max_length=100)
    zip_code = forms.CharField(required=True, label=u"zip code", max_length=100)
    state = forms.CharField(required=True, max_length=100)


class RegisterForm(forms.Form):
    error_messages = {
        'duplicate_email': 'A user with that email already exists.',
        'password_allnumber': 'The password cannot be numbers only',
        'password_mismatch': 'The two password fields didn\'t match.'
    }

    username = forms.CharField(label='username', max_length=50, required=True)
    password = forms.CharField(label='password', widget=forms.PasswordInput(), required=True, min_length=pwd_min_length)
    password_confirm = forms.CharField(label='password_confirm', widget=forms.PasswordInput(), required=True,
                                       min_length=pwd_min_length)
    email = forms.EmailField(label='email', required=True)
    first_name = forms.CharField(label='first_name', max_length=50)
    last_name = forms.CharField(label='last_name', max_length=50)

    # def clean_email(self):
    #     ########################
    #     # may need modification#
    #     ########################
    #     ret = self.objects.filter(username=self.cleaned_data.get("username"))
    #     # ret = models.UserInfor.objects.filter(username=self.cleaned_data.get("username"))
    #     if not ret:
    #         return self.cleaned_data.get("username")
    #     else:
    #         raise forms.ValidationError(
    #             self.error_messages['duplicate_email'],
    #             code='duplicate_email',
    #         )

    def clean_password(self):
        data = self.cleaned_data.get("password")
        if not data.isdigit():
            return self.cleaned_data.get("password")
        else:
            raise forms.ValidationError(
                self.error_messages['password_allnumber'],
                code='password_allnumber',
            )

    def clean(self):
        if self.cleaned_data.get("password") == self.cleaned_data.get("password_confirm"):
            return self.cleaned_data

        else:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )


class MyPasswordResetForm(PasswordResetForm):

    email = forms.EmailField()

    # email not registered warning
    def clean_email(self):
        email = self.cleaned_data.get('email', '')
        if not UserInfo.objects.filter(email=email):
            raise forms.ValidationError('The email address is not registered!')
        return email

# attrs={'size': 10, 'title': 'Your name'}