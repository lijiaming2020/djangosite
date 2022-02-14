from django import forms
from django.contrib.auth.models import User
from .models import User_Info

class UserLoginForm(forms.Form):
    username=forms.CharField()
    password=forms.CharField(label='密码')

class UserRegisterForm(forms.ModelForm):
    password=forms.CharField(label='密码',required=True)
    password2=forms.CharField()
    class Meta:
        model=User
        fields=('username','email',)
    def clean_password(self):
        data=self.cleaned_data
        if data.get('password')==self['password2'].value():
            return data.get('password')
        else:
            raise forms.ValidationError('密码输入不一致!!!')

class User_detailForm(forms.ModelForm):
    class Meta:
        model=User_Info
        fields='__all__'
        exclude=['user']
