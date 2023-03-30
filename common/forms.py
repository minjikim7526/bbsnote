# 인증 기능 가져다 쓴다

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

# django의 auth앱이 제공해주는 UserCreationForm을 상속받는 클래스를 만든다
class UserForm(UserCreationForm):
    email = forms.EmailField(label="이메일")
    # 이름도 받고 싶으면 추가하면 됨


    class Meta:
        model = User
        fields = ("username", "email")