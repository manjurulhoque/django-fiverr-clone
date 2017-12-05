import datetime
from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
from django.forms.extras.widgets import SelectDateWidget
from .models import User

from .models import Gig


class GigForm(forms.ModelForm):
    class Meta:
        model = Gig
        fields = ['title', 'category', 'description', 'price', 'photo', 'status']


class UserLoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self, *args, **kwargs):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")

        if email and password:
            user = authenticate(email=email, password=password)
            if not user:
                raise forms.ValidationError("User Does Not Exist.")
            if not user.check_password(password):
                raise forms.ValidationError("Password Does not Match.")
            if not user.is_active:
                raise forms.ValidationError("User is not Active.")

        return super(UserLoginForm, self).clean(*args, **kwargs)


class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username",
                  "email",
                  "password1",
                  "password2")

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.username = self.cleaned_data['username']
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user