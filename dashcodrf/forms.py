from django import forms
from django.contrib.auth.models import User

from dashcodrf.models import Client, Branch, RoutePlan


class PersonalInfo(forms.ModelForm):
    username = forms.CharField(max_length=15, widget=forms.TextInput(
        attrs={'class': 'dash-input', 'placeholder': 'Enter your username'}))
    email = forms.EmailField(max_length=50,
                             widget=forms.EmailInput(attrs={'class': 'dash-input', 'placeholder': 'Enter your email'}))

    class Meta:
        model = User
        fields = ('username', 'email')


class PasswordChange(forms.ModelForm):
    password = forms.CharField(label='Current Password', max_length=50, min_length=8,
                               widget=forms.PasswordInput(
                                   attrs={'class': 'dash-input', 'placeholder': 'Enter current password'}))
    new_password = forms.CharField(max_length=50, min_length=8,
                                   widget=forms.PasswordInput(
                                       attrs={'class': 'dash-input', 'placeholder': 'Enter new password'}))
    confirm_password = forms.CharField(max_length=50, min_length=8,
                                       widget=forms.PasswordInput(
                                           attrs={'class': 'dash-input', 'placeholder': 'Repeat new password'}))

    class Meta:
        model = User
        fields = ('password',)


class NewUser(forms.ModelForm):
    first_name = forms.CharField(max_length=15, widget=forms.TextInput(
        attrs={'class': 'dash-input', 'placeholder': 'Enter first name'}))
    last_name = forms.CharField(max_length=15, widget=forms.TextInput(
        attrs={'class': 'dash-input', 'placeholder': 'Enter last name'}))

    class Meta:
        model = User
        fields = ['first_name', 'last_name']


class NewStaff(forms.ModelForm):
    username = forms.CharField(max_length=15, widget=forms.TextInput(
        attrs={'class': 'dash-input', 'placeholder': 'Enter username'}))
    first_name = forms.CharField(max_length=15, widget=forms.TextInput(
        attrs={'class': 'dash-input', 'placeholder': 'Enter first name'}))
    last_name = forms.CharField(max_length=15, widget=forms.TextInput(
        attrs={'class': 'dash-input', 'placeholder': 'Enter last name'}))
    email = forms.EmailField(max_length=50,
                             widget=forms.EmailInput(
                                 attrs={'class': 'dash-input', 'placeholder': 'Enter email address'}))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email']


class NewClient(forms.ModelForm):
    first_name = forms.CharField(max_length=15, widget=forms.TextInput(
        attrs={'class': 'dash-input', 'placeholder': 'Enter first name'}))
    last_name = forms.CharField(max_length=15, widget=forms.TextInput(
        attrs={'class': 'dash-input', 'placeholder': 'Enter last name'}))
    phone_number = forms.CharField(max_length=15, widget=forms.TextInput(
        attrs={'class': 'dash-input', 'placeholder': 'Enter phone number'}))
    national_id = forms.CharField(max_length=15, widget=forms.TextInput(
        attrs={'class': 'dash-input', 'placeholder': 'Enter national ID'}))
    email = forms.EmailField(max_length=50,
                             widget=forms.EmailInput(
                                 attrs={'class': 'dash-input', 'placeholder': 'Enter email address'}))
    dob = forms.CharField(label='Date of Birth', max_length=15, widget=forms.TextInput(
        attrs={'class': 'dash-input', 'placeholder': 'Enter date of birth'}))

    class Meta:
        model = Client
        fields = ['phone_number', 'email', 'first_name', 'last_name', 'dob', 'national_id']


class NewBranch(forms.ModelForm):
    name = forms.CharField(max_length=15, widget=forms.TextInput(
        attrs={'class': 'dash-input', 'placeholder': 'Enter branch name'}))

    class Meta:
        model = Branch
        fields = ['name']


class BranchStaff(forms.Form):
    branch_user = forms.IntegerField(widget=forms.Select(attrs={'class': 'dash-input'}))


class NewRoutePlan(forms.ModelForm):
    title = forms.CharField(max_length=128, widget=forms.TextInput(
        attrs={'class': 'dash-input', 'placeholder': 'Enter a title'}))
    plan_user = forms.IntegerField(widget=forms.Select(attrs={'class': 'dash-input'}))
    visit_date = forms.CharField(max_length=15, widget=forms.TextInput(
        attrs={'class': 'dash-input flatpickr-input', 'placeholder': 'Enter visit date'}))
    location = forms.CharField(max_length=50,
                               widget=forms.TextInput(
                                   attrs={'class': 'dash-input', 'placeholder': 'Enter location'}))

    class Meta:
        model = RoutePlan
        fields = ['title', 'visit_date', 'location']
