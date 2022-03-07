from django import forms
from django.contrib.auth.forms import UserCreationForm
from users.models import Members, Ugenres

# from django.contrib.auth.models import User // 초기 설정

CHOICES = [
        ('ME', '1'),
        ('YOU', '2'),
        ('WE', '3'),
    ]


class UserForm(UserCreationForm):
    # 입력받을 이메일 필드 추가하기
    email = forms.EmailField(label="이메일")

    # Members 클래스와 관련시키기 (필드 연결)
    class Meta:
        model = Members
        # fields = ("username", "email", "u_mobile", "u_image")
        fields = ["username", "email", "u_mobile"]
        
    # 초기 설정 (User=>Members로 교체 후 오류 배제)
    # class Meta:
    #     model = User
    #     fields = ("username", "email")


class UpdateForm(forms.ModelForm):
    class Meta:
        model = Members
        fields = ['username', 'email', 'u_mobile', 'u_image']

        labels = {
            'username': '사용자 이름',
            'email': '이메일 주소',
            'u_mobile': '전화번호',
            'u_image': '프로필 이미지',
        }

        widgets = {
            'username': forms.TextInput(
                attrs={
                    'class': 'form-control w-25',
                }
            ),
            'email': forms.TextInput(
                attrs={
                    'class': 'form-control w-25',
                }
            ),
            'u_mobile': forms.TextInput(
                attrs={
                    'class': 'form-control w-25',
                }
            )
        }


class GenreForm(forms.ModelForm):
    class Meta:
        model = Ugenres
        fields = ['ug_genre']

        labels = {
            'ug_genre': '선호 장르',
        }
        # exclude = ('---------',)
        widgets = {
            'ug_genre': forms.CheckboxSelectMultiple(),
        }
        # widget = forms.Select(choices=CHOICES)
        # genres = forms.MultipleChoiceField(
        #     # queryset=Ugenres.objects.all(),
        #     # widget=forms.CheckboxSelectMultiple,
        #
        # )



