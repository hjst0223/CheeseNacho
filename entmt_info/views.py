from django.shortcuts import render, redirect, get_object_or_404
from entmt_info.models import Movies, Series, Genres
from entmt_manage.models import Mcomment, Scomment, Mgenres, Sgenres
from entmt_info.forms import CommentForm
from django.contrib import messages
from users.models import Members

# from entmt_info.forms import PostSearchForm
# from django.views.generic import FormView
# from django import forms
# from django.http import HttpResponse, HttpResponseRedirect


from entmt_info import api_python   # api 관련 함수 모음
from django.db.models import Q      # 두개이상의 인자를 사용해 검색할 경우
import csv


# Create your views here.

def ei_page(request):
    code = 634649
    return render(request, 'entmt_info/import_data.html')

# 장르리스트 import
def ei_genre(request):
    url_movies = 'https://api.themoviedb.org/3/genre/movie/list'
    url_tv = 'https://api.themoviedb.org/3/genre/tv/list'
    for url in [url_movies, url_tv]:
        result = api_python.api_genre(url)
        for value in result:
            # Primary Key라서 try-excetp 구문이 필요없음
            # try:
            #     Genres.objects.get(genre_id=value['id'])
            # except:
            genre = Genres()
            genre.genre_id = value['id']
            genre.g_name = value['name']
            genre.save()
    return redirect('entmt_info:ei_page')


# 영화 세부정보, genre import
def ei_movie(request):
    movie_csv = 'entmt_info/data/movie_200.csv'

    with open(movie_csv, 'r', encoding='utf-8') as f:
        rdr = csv.reader(f)
        for line in rdr:
            print(line[0]) # 문제 생길것에 대비해 print
            url_movies = 'https://api.themoviedb.org/3/movie/' + line[0]
            result = api_python.api_movie(url_movies)

            # movie model 객체 생성
            movie = Movies()
            movie.movie_id = result['id']
            movie.m_title = result['original_title']
            movie.m_posterPath = result['poster_path']
            movie.m_releaseDate = result['release_date']
            movie.m_popularity = result['popularity']
            movie.save()

            # Genre model 객체 생성
            Movie = Movies.objects.get(movie_id=result['id'])
            for v in result['genres']:
                Genre = Genres.objects.get(genre_id=v['id'])
                # Primary Key 가 없어서 자동으로 중복제외를 해주지 않아 try-except 구문으로 해줌
                try:
                    Mgenres.objects.get(Q(mg_movie=result['id']) & Q(mg_genre=v['id']))
                except:
                    m_genre = Mgenres()
                    m_genre.mg_movie = Movie
                    m_genre.mg_genre = Genre
                    m_genre.save()

    # f.close() # with open으로 해서 close 필요 없음
    return redirect('entmt_info:ei_page')


# poster path가 null인 값이 있어 오류가 납니다.
# model의 poster path의 null 수정 후 돌려주세요 ㅠㅠ
def ei_tv(request):
    tv_csv = 'entmt_info/data/tv_200.csv'

    with open(tv_csv, 'r', encoding='utf-8') as f:
        rdr = csv.reader(f)
        for line in rdr:
            print(line[0])
            url_series = 'https://api.themoviedb.org/3/tv/' + line[0]
            result = api_python.api_tv(url_series)

            # movie model 객체 생성
            series = Series()
            series.series_id = result['id']
            series.s_title = result['original_name']
            series.s_posterPath = result['poster_path']
            series.s_firstAirDate = result['first_air_date']
            series.s_lastAirDate = result['last_air_date']
            series.s_popularity = result['popularity']
            series.save()

            # Genre model 객체 생성
            Series_e = Series.objects.get(series_id=result['id'])
            for v in result['genres']:
                Genre = Genres.objects.get(genre_id=v['id'])
                # Primary Key 가 없어서 자동으로 중복제외를 해주지 않아 try-except 구문으로 해줌
                try:
                    Sgenres.objects.get(Q(sg_series=result['id']) & Q(sg_genre=v['id']))
                except:
                    s_genre = Sgenres()
                    s_genre.sg_series = Series_e
                    s_genre.sg_genre = Genre
                    s_genre.save()

    # f.close()
    return redirect('entmt_info:ei_page')


# 상세 정보 페이지
def e_detail(request):
    url_movies = 'https://api.themoviedb.org/3/movie/'
    url_tv = 'https://api.themoviedb.org/3/tv/'
    if request.GET.get('media_type') == 'movie':
        result = api_python.api_detail(url_movies + request.GET.get('res_id'))
        comments = Mcomment.objects.filter(mc_movie=request.GET.get('res_id'))

    elif request.GET.get('media_type') == 'tv':
        result = api_python.api_detail(url_tv + request.GET.get('res_id'))
        comments = Scomment.objects.filter(sc_movie=request.GET.get('res_id'))
    else:
        print('movie, tv 이외의 거라서 구현이 안되어있어요!')

    content = {
        'results': result,
        'comments': comments
    }
    return render(request, 'entmt_info/detail.html', content)


# 검색 결과 페이지
def e_results(request):
    search_word = request.GET.get('search', '')
    result = api_python.api_search(search_word)

    # result 순서에 맞춰서 img Form list를 만들어 같이 content에 주는 방식으로 도전
    # html에서 직접 불러오는 방식으로 쓰기로 결정
    # img_form = [api_python.api_img(result_img['poster_path']) for result_img in result]
    # img_form = api_python.api_img(result[0]['poster_path'])

    # 장르 한글로 변경
    for i in range(len(result)):
        for j in range(len(result[i]['genre_ids'])):
            # print(result[i]['genre_ids'][j])
            # print(Genres.objects.get(genre_id=result[i]['genre_ids'][j]).g_name)
            result[i]['genre_ids'][j] = Genres.objects.get(genre_id=result[i]['genre_ids'][j]).g_name

    content = {
        'results': result,
        # 'images': img_form
    }

    return render(request, 'entmt_info/results.html', content)


# 댓글 등록
def submit_comment(request, movie_id):
    # 현재 페이지 url
    url = request.META.get('HTTP_REFERER')

    if request.method == 'POST':
        # 기존 리뷰를 업데이트하는 경우
        if Mcomment.objects.filter(pk=movie_id):

            # filter에 객체가 존재하는 경우 업데이트
            comments = Mcomment.objects.filter(pk=movie_id)
            form = CommentForm(request.POST, instance=comments)
            form.save()
            messages.success(request, '리뷰가 업데이트되었습니다!')
            return redirect(url)

        # 새 리뷰를 등록하는 경우
        else:
            # 필터에 객체가 없는 경우 새로 등록
            form = CommentForm(request.POST)
            if form.is_valid():
                user = Members.objects.get(pk=request.user.id)
                movie = Movies.objects.get(pk=movie_id)

                data = Mcomment()
                data.mc_title = form.cleaned_data['mc_title']
                data.mc_star = form.cleaned_data['mc_star']
                data.mc_content = form.cleaned_data['mc_content']
                data.mc_movie = movie
                data.mc_member = user
                data.save()
                messages.success(request, '리뷰가 등록되었습니다!')

                return redirect(url)
            else:
                messages.error(request, '오류!')

