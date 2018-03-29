from django import forms
class LoginForm(forms.Form):
    username = forms.CharField(required=True,max_length=100)
    password = forms.CharField(required=True,max_length=100)
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
        widget=forms.PasswordInput(),
    )
    new_password2 = forms.CharField(
        required=True,
        max_length=100,
        label=u"confirm new password",
        widget=forms.PasswordInput(),
    )
class EdituserinfoForm(forms.Form):
    first_name = forms.CharField(required=True,max_length=100,label=u"first name")
    last_name = forms.CharField(required=True,max_length=100, label=u"last name" )
    email = forms.EmailField(max_length=100,label=u"email")
    phone = forms.IntegerField(required=True,label=u"phone")
    address = forms.CharField(required=True, max_length=100,label=u"address")
    city = forms.CharField(required=True,max_length=100,label=u"city")
    gender = forms.CharField(required=True,max_length=100)
    zip_code = forms.CharField(required=True,label=u"zip code",max_length=100)
    state = forms.CharField(required=True,max_length=100)