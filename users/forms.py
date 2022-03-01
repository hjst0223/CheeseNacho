from django import forms
from django.contrib.auth.forms import UserCreationForm
from users.models import Members
# from django.contrib.auth.models import User // 초기 설정


class UserForm(UserCreationForm):
    # 입력받을 이메일 필드 추가하기
    email = forms.EmailField(label="이메일")

    # Members 클래스와 관련시키기 (필드 연결)
    class Meta:
        model = Members
        fields = ("username", "email", "u_mobile", "u_image")
        
    # 초기 설정 (User=>Members로 교체 후 오류 배제)
    # class Meta:
    #     model = User
    #     fields = ("username", "email")

   

