from django import forms
from django.contrib.auth.models import User


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class RegisterForm(forms.ModelForm):
    password = forms.CharField(label='password', widget=forms.PasswordInput)
    repassword = forms.CharField(label='repassword', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username',)

    def clean_repassword(self):
        cd = self.cleaned_data
        if cd['password'] != cd['repassword']:
            raise forms.ValidationError('两次密码输入不一致')
        return cd['repassword']
