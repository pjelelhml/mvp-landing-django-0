from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()


class LoginForm(forms.Form):
    username = forms.CharField(label='', widget=forms.TextInput(
        attrs={'placeholder': 'Your username'}))
    password = forms.CharField(label='', widget=forms.PasswordInput(
        attrs={'placeholder': 'Your password'}))

    # def clean_username(self):
    #     username = self.cleaned_data.get("username")

    #     return username


class RegisterForm(forms.ModelForm):
    username = forms.CharField(label='Username', widget=forms.TextInput(
        attrs={'placeholder': 'Your username'}))
    email = forms.EmailField(widget=forms.EmailInput(
        attrs={'placeholder': 'Your email'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(
        attrs={'placeholder': 'Your password'}))
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput(
        attrs={'placeholder': 'Confirm password'}))

    class Meta:
        model = User
        fields = [
            'username',
            'email'
        ]

    def clean(self):
        data = self.cleaned_data
        password_1 = data.get("password")
        password_2 = data.get("password2")
        if password_1 != password_2:
            # assign to non_field_error
            raise forms.ValidationError("passwords must match!")
        return data

    def clean_username(self):
        username = self.cleaned_data.get("username")
        qs = User.objects.filter(username__iexact=username)
        if qs.exists():
            raise forms.ValidationError(f"{username} is taken. Try again")
        return username

    def clean_email(self):
        email = self.cleaned_data.get("email")
        qs = User.objects.filter(email__iexact=email)
        if qs.exists():
            raise forms.ValidationError(f"{email} is taken. Try again")
        return email
