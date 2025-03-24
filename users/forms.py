from django import forms
from users.models import User
# from django.contrib.auth.forms import UserCreationForm

style = 'w-full px-3 py-1 border rounded-lg focus:outline-none focus:ring-1 focus:ring-blue-500'

class SignupForm(forms.ModelForm):
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': style, 'placeholder': 'First Name'}),
        required=True
    )
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': style, 'placeholder': 'Last Name'}),
        required=True
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': style, 'placeholder': 'email'})
    )
    iin = forms.CharField(
        widget=forms.TextInput(attrs={'class': style, 'placeholder': 'IIN'}),
        required=True
    )
    phone = forms.CharField(
        widget=forms.TextInput(attrs={'class': style, 'placeholder': 'Phone'}),
        required=True
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': style, 'placeholder': 'Password'}),
        required=True
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': style, 'placeholder': 'Confirm Password'}),
        required=True
    )

    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "iin", "phone"]

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            self.add_error("confirm_password", "Passwords do not match!")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

class UserLoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={'class': style, 'placeholder': 'email'}
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'class': style, 'placeholder': 'password'}
        )
    )