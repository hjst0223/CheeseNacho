from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from users.forms import UserForm, GenreForm
from .forms import UpdateForm
from django.contrib.auth.hashers import check_password
from django.contrib import messages, auth
# from django.views.decorators.csrf import csrf_exempt

from users.models import Mlike, Slike, Ugenres
from entmt_info.models import Movies, Series, Genres
from django.db.models import Q


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

            # 입력받은 username, password로 로그인하기
            user = authenticate(username=username, password=raw_password)
            login(request, user)

            # 회원가입 후 로그인 상태로 메인 페이지 돌아가기
            return redirect('users:edit_genre')
    else:
        form = UserForm()
    return render(request, 'users/signup.html', {'form': form})


def mypage(request):
    user_id = request.user.id
    mlike_list = Mlike.objects.filter(ml_member=user_id)
    slike_list = Slike.objects.filter(sl_member=user_id)
    movie_list = []
    series_list = []

    for mlike in mlike_list:
        # mlike_code_list.append(mlike.ml_movie_id)
        movie_list.append(Movies.objects.get(movie_id=mlike.ml_movie_id))
        # print(f'--{mlike}({mlike.ml_movie_id})={movie_list}')
    for slike in slike_list:
        series_list.append(Series.objects.get(series_id=slike.sl_series_id))

    content = {
        'movie_list': movie_list,
        'series_list': series_list
    }
    return render(request, 'users/mypage.html', content)


def change_password(request):
    if request.method == "POST":
        user = request.user
        origin_password = request.POST["origin_password"]
        if check_password(origin_password, user.password):
            new_password = request.POST["new_password"]
            confirm_password = request.POST["confirm_password"]
            if new_password == confirm_password:
                user.set_password(new_password)
                user.save()
                auth.login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                messages.success(request, '비밀번호가 변경되었습니다!')
                return redirect('users:change_password')
            else:
                messages.error(request, '비밀번호가 다릅니다!')
        else:
            messages.error(request, '비밀번호를 잘못 입력하셨습니다.')
        return render(request, 'users/change_password.html')
    else:
        return render(request, 'users/change_password.html')


def update(request):
    if request.method == 'POST':
        update_form = UpdateForm(request.POST,
                                 request.FILES, instance=request.user)

        if update_form.is_valid():
            update_form.save()
            messages.success(request, '회원정보가 변경되었습니다!')
            return redirect('users:update')

    else:
        update_form = UpdateForm(instance=request.user)

    context = {
        'update_form': update_form
    }
    return render(request, 'users/update.html', context)


# def genre(request):
#     if request.method == 'POST':
#         genre_form = GenreForm(request.POST, instance=request.user)
#         print('----------------------------------------------------')
#         # print(genre_form)
#
#         if genre_form.is_valid():
#             print('ㅇ오')
#             genre_form.save()
#             messages.success(request, '선호 장르가 업데이트되었습니다!')
#             return redirect('users:genre')
#
#     else:
#         genre_form = GenreForm(instance=request.user)
#
#     context = {
#         'genre_form': genre_form
#     }
#     return render(request, 'users/genre.html', context)


def genre(request):
    genres = Genres.objects.all()
    genre_list = []
    for genre in genres:
        if Ugenres.objects.filter(Q(ug_genre=genre) & Q(ug_member=request.user)).exists():
            genre_list.append({'genre': genre, 'status': True})
        else: genre_list.append({'genre': genre, 'status': False})
    print(genre_list)
    context = {
            'genres': genre_list
        }
    return render(request, 'users/genre.html', context)


def edit_genre(request):

    if request.method == 'POST':
        selected = request.POST.getlist('selected')
        ugenres = Ugenres.objects.filter(ug_member=request.user)
        selected_ug = [str(ugenre.ug_genre.genre_id) for ugenre in ugenres]
        code_list = list(set(selected + selected_ug))
        print(selected)
        print(selected_ug)
        print(code_list)

        # selected, selected_ug 둘다있는거 pass
        # selected 에는 있고, selected_ug에는 없는거 save()
        # selected 에는 없고, selected_ug에는 있는거 delete()

        for code in code_list:
            genre = Genres.objects.get(pk=code)
            if (code in selected) and (code not in selected_ug):
                # if Ugenres.objects.filter(Q(ug_genre=genre) & Q(ug_member=request.user)).exists():
                #     pass # 필요는 없지만 혹시나 해서
                # else:
                ugenre = Ugenres()
                ugenre.ug_genre = genre
                ugenre.ug_member = request.user
                ugenre.save()

            elif (code not in selected) and (code in selected_ug):
                ugenre = Ugenres.objects.get(Q(ug_genre=genre) & Q(ug_member=request.user))
                ugenre.delete()
            else : pass


        messages.success(request, '선호 장르가 업데이트되었습니다!')
        print('ok')

    return redirect('users:genre')