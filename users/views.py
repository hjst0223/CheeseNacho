from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from users.forms import UserForm
# from django.views.decorators.csrf import csrf_exempt
# from users.models import Members

# csrf token의 다른 방법
# @csrf_exempt

# 회원가입
def signup(request):
    # POST 방식의 request일 경우
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')

            # 프로필 이미지 저장해서 user 정보 만드는 다른 방식
            # email = request.POST.get('email')
            # mobile = request.POST.get('u_mobile')
            # img = request.FILES.get('u_image')
            # Members.objects.create_user(username=username, password=raw_password,
            #                             email=email, u_mobile=mobile, u_image=img)
            # return redirect('users:login')

            # 입력받은 username, password로 로그인하기
            user = authenticate(username=username, password=raw_password)
            login(request, user)

            # 회원가입 후 로그인 상태로 메인 페이지 돌아가기
            return redirect('home')
    else:
        form = UserForm()
    return render(request, 'users/signup.html', {'form': form})


def mypage(request):

    return render(request, 'users/mypage.html')
