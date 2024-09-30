from builtins import super
from django.forms import DateTimeField

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from .models import Profile, UserTransaction, Bank, Transfer
from django.forms import ModelChoiceField

User = get_user_model()


class RegisterForm(forms.ModelForm):
    password1 = forms.CharField(label='password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = (
            'email',
            'full_name'
        )

    def clean_password(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(widget=forms.TextInput(attrs={
        'placeholder': 'email@',
        'class': 'form-control'}))
    full_name = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'FULL NAME',
        'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['full_name', 'email']


class UserAdminChangeForm(forms.ModelForm):
    """a form for updating users. includes all the fields on the user, but replaces the password field with admin's password hash display """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('email', 'full_name', 'password', 'active', 'admin')

    def clean_password(self):
        return self.initial["password"]


class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.TextInput(attrs={
        'placeholder': 'user id',
        'class': 'form-control'

    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'INSERT PASSWORD'
    }))


class ProductForm(forms.ModelForm):
    amount = forms.CharField(widget=forms.NumberInput(attrs={
        'placeholder': 'amount',
        'class': 'form-control'
    }))
    status = forms.EmailField(widget=forms.TextInput(attrs={
        'placeholder': 'status',
        'class': 'form-control'}))
    event_date = DateTimeField(input_formats=["%d %b %Y %H:%M:%S %Z"])

    class Meta:
        model = Transfer
        fields = ['transfer_date', 'amount', 'status', ]


class TransferForm(forms.Form):
    user_identity = forms.CharField(widget=forms.NumberInput(attrs={
        'placeholder': 'Account number',
        'class': 'form-control'
    }))
    pin = forms.CharField(widget=forms.NumberInput(attrs={
        'placeholder': 'pin',
        'class': 'form-control'
    }))
    amount = forms.CharField(widget=forms.NumberInput(attrs={
        'placeholder': 'amount',
        'class': 'form-control'
    }))
    description = forms.CharField(widget=forms.Textarea(attrs={
        'rows': 3,
        'placeholder': 'transaction description',
        'class': 'form-control'
    }))
    bank = forms.ModelChoiceField(widget=forms.Select(attrs={
        'class': 'form-control',
        'placeholder': 'select bank'
    }), queryset=Bank.objects.all(), to_field_name="bank")

class PinForm(forms.Form):
    pin = forms.CharField(widget=forms.NumberInput(attrs={
        'placeholder': 'pin',
        'class': 'form-control'
    }))
    newpin = forms.CharField(widget=forms.NumberInput(attrs={
        'placeholder': 'New pin',
        'class': 'form-control'
    }))

class RequestForm(forms.Form):
    amount = forms.CharField(widget=forms.NumberInput(attrs={
        'placeholder': 'amount',
        'class': 'form-control'
    }))
    description = forms.CharField(widget=forms.Textarea(attrs={
        'rows': 3,
        'placeholder': 'transaction description',
        'class': 'form-control'
    }))


def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.fields['categories'].queryset = Bank.objects.none()


class BanksForm(forms.ModelForm):
    name = forms.CharField()

    class Meta:
        model = Bank
        fields = '__all__'

class ProfileUpDateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = []



