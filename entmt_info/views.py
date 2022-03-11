from django.shortcuts import render, redirect, get_object_or_404
from entmt_info.models import Movies, Series, Genres
from entmt_manage.models import Mcomment, Scomment, Mgenres, Sgenres
from entmt_info.forms import McommentForm, ScommentForm
from django.contrib import messages
from users.models import Members, Ugenres
from entmt_manage.models import Mgenres, Sgenres
from users.models import Mlike, Slike

from entmt_info import api_python   # api 관련 함수 모음
from django.db.models import Q      # 두개이상의 인자를 사용해 검색할 경우
import csv


# Create your views here.

def homepage(request):
    # 인기영화 8개, 인기시리즈 8개 보여주기
    # 로그인 인증 되어있을 시, 내 추천장르 : 4개 가져와서 장르별 가져오기
    # 로그인 인증 되어있지 않을 시, 인기 장르 중 4개 가져와서 장르별 가져오기
    pop_movies = Movies.objects.all().order_by('-m_popularity')[:8]
    movies_genres = [Mgenres.objects.filter(mg_movie=movie) for movie in pop_movies]
    pop_series = Series.objects.all().order_by('-s_popularity')[:8]
    series_genres = [Sgenres.objects.filter(sg_series=series) for series in pop_series]
    pop_movies_genres = [{'movie': movie, 'genre': genre}
                         for movie, genre in zip(pop_movies, movies_genres)]
    pop_series_genres = [{'series': series, 'genre': genre}
                         for series, genre in zip(pop_series, series_genres)]
    print(pop_movies_genres)
    print('-----hello-------')
    try:
        # autho가 선택한 genre 가져오기
        pop_genres = Ugenres.objects.filter(ug_member=request.user)[:4]
        pop_genres_f = pop_genres[0]
        pop_genres = pop_genres[1:4]
        # 장르에 해당하는 media 가져오기
        genre_movies_f = Mgenres.objects.filter(mg_genre=pop_genres_f.ug_genre)[:8]
        genre_movies = [Mgenres.objects.filter(mg_genre=genre.ug_genre)[:8] for genre in pop_genres]
        genre_series_f = Sgenres.objects.filter(sg_genre=pop_genres_f.ug_genre)[:4]
        genre_series = [Sgenres.objects.filter(sg_genre=genre.ug_genre)[:4] for genre in pop_genres]
        genre_media = [{'genre': genre, 'movie': g_movie, 'series': g_series}
                       for genre, g_movie, g_series in zip(pop_genres, genre_movies, genre_series)]
        print(f'---user:{request.user}---')

    except:
        # 현재 저장되어있는 장르 순위 출력,,, 단점 : 지금현재 Mgenre로만 순위가 매겨져 있음
        pop_genres = [[genre.genre_id, genre.g_name, Mgenres.objects.filter(mg_genre=genre).count()] for genre in
                      Genres.objects.all()]
        pop_genres.sort(key=lambda x: -x[2])
        # print(pop_genres)
        # pop_genres2 = [[genre.genre_id, genre.g_name, Sgenres.objects.filter(sg_genre=genre).count()] for genre in
        #               Genres.objects.all()]
        # pop_genres2.sort(key=lambda x: -x[2])
        # print(pop_genres2)
        pop_genres_match = [Genres.objects.get(genre_id=genre[0]) for genre in pop_genres]
        pop_genres_f = pop_genres_match[0]
        pop_genres = pop_genres_match[1:4]
        # 장르에 해당하는 media 가져오기
        genre_movies_f = Mgenres.objects.filter(mg_genre=pop_genres_f)[:8]
        genre_movies = [Mgenres.objects.filter(mg_genre=genre)[:8] for genre in pop_genres]
        genre_series_f = Sgenres.objects.filter(sg_genre=pop_genres_f)[:4]
        genre_series = [Sgenres.objects.filter(sg_genre=genre)[:4] for genre in pop_genres]
        genre_media = [{'genre': genre, 'movie': g_movie, 'series': g_series}
                       for genre, g_movie, g_series in zip(pop_genres, genre_movies, genre_series)]
        print('---AnonymousUser---')

    context = {
        # 'pop_movies': pop_movies,
        # 'pop_series': pop_series,
        'pop_movies_genres': pop_movies_genres,
        'pop_series_genres': pop_series_genres,
        'pop_genres_f': pop_genres_f,
        'genre_movies_f': genre_movies_f,
        'genre_series_f': genre_series_f,
        'genre_media': genre_media,
    }
    return render(request, 'entmt_info/homepage.html', context)


    # print(genre_movies_f)
    # print(f'----pop_genres_f : {pop_genres_f}')
    # print(f'----pop_genres : {pop_genres}')
    # print(f'----pop_movies : {pop_movies}')
    # # print(f'----pop_genres_match : {pop_genres_match[:4]}')
    # print(f'----genre_movies_f : {genre_movies_f}')
    # print(f'----genre_movies : {genre_movies}')
    # print(f'----genre_series : {genre_series}')
    # print(f'----genre_media : {genre_media}')


def ei_page(request):
    # code = 634649
    return render(request, 'entmt_info/import_data.html')

# 장르리스트 import
def ei_genre(request):
    url_movie_genres = 'https://api.themoviedb.org/3/genre/movie/list'
    url_series_genres = 'https://api.themoviedb.org/3/genre/tv/list'
    for url in [url_movie_genres, url_series_genres]:
        result = api_python.api_genre(url)
        for value in result:
            genre = Genres()
            genre.genre_id = value['id']
            genre.g_name = value['name']
            genre.save()
    print('done - downloading genre')
    return redirect('entmt_info:ei_page')

# db save code for movies
def dbsave_movie(result):

    # Movies model 객체 생성
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

# db save code for series
def dbsave_series(result):

    # Series model 객체 생성
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


# add movie object, add genre object
def ei_movie(request):
    movie_csv = 'entmt_info/data/movie_200.csv'

    with open(movie_csv, 'r', encoding='utf-8') as f:
        rdr = csv.reader(f)
        for line in rdr:
            url_movies = 'https://api.themoviedb.org/3/movie/' + line[0]
            result = api_python.api_request(url_movies)

            # db에 추가
            dbsave_movie(result)

    print('done - downloading movies')

    return redirect('entmt_info:ei_page')


# add series object, add genre object
def ei_tv(request):
    tv_csv = 'entmt_info/data/tv_200.csv'

    with open(tv_csv, 'r', encoding='utf-8') as f:
        rdr = csv.reader(f)
        for line in rdr:
            url_series = 'https://api.themoviedb.org/3/tv/' + line[0]
            result = api_python.api_request(url_series)

            # db에 추가
            dbsave_series(result)

    print('done - downloading series')

    return redirect('entmt_info:ei_page')


# 상세 정보 페이지
# media_type과 response_id 필요
def e_detail(request):
    url_movies = 'https://api.themoviedb.org/3/movie/'
    url_tv = 'https://api.themoviedb.org/3/tv/'
    res_id = request.GET.get('res_id')
    media_type = request.GET.get('media_type')

    if media_type == 'movie':
        result = api_python.api_request(url_movies + res_id)

        # DB에 존재하지 않을 경우 넣어줌
        if Movies.objects.filter(movie_id=res_id).exists() == False:
            dbsave_movie(result)

        try: comments = Mcomment.objects.filter(Q(mc_movie=result['id']) & ~Q(mc_member=request.user))
        except: comments = Mcomment.objects.filter(mc_movie=result['id'])

        # like_count = Movies.objects.get(movie_id=result['id']).m_likeCount
        like_count = Mlike.objects.filter(ml_movie=result['id']).count()

        # 로그인되지 않았을 때 생기는 오류 수정
        try: like_status = Mlike.objects.filter(Q(ml_movie=result['id']) & Q(ml_member=request.user)).exists()
        except: like_status = False

        try:
            comment_status = Mcomment.objects.filter(Q(mc_movie=result['id']) & Q(mc_member=request.user))
            comment_status = comment_status[0]
        except: comment_status = False
        # print(comment_status)
        # if(Mcomment.objects.filter(Q(ml_movie=result['id']) & Q(ml_member=request.user))):
        #     comment_status = True

    elif media_type == 'tv':
        result = api_python.api_request(url_tv + res_id)

        # DB에 존재하지 않을 경우 넣어줌
        if Series.objects.filter(series_id=res_id).exists() == False:
            dbsave_series(result)

        try: comments = Scomment.objects.filter(Q(sc_series=result['id']) & ~Q(sc_member=request.user))
        except: comments = Scomment.objects.filter(sc_series=result['id'])

        # like_count = Series.objects.get(series_id=result['id']).s_likeCount
        like_count = Slike.objects.filter(sl_series=result['id']).count()

        # 로그인되지 않았을 때 생기는 오류 수정
        try: like_status = Slike.objects.filter(Q(sl_series=result['id']) & Q(sl_member=request.user)).exists()
        except: like_status = False

        # 일단 넣었는데 오류나는지 확인해봐야함
        try:
            comment_status = Scomment.objects.filter(Q(sc_series=result['id']) & Q(sc_member=request.user))
            comment_status = comment_status[0]
        except: comment_status = False

    else:
        print('movie, tv 이외의 거라서 구현이 안되어있어요!')
        print(media_type)

    print(result)
    content = {
        'results': result,
        'comments': comments,
        'like_count': like_count,
        'like_status': like_status,
        'media_type': media_type,
        'comment_status': comment_status,
    }
    # return render(request, 'entmt_info/detail.html', content)
    # return render(request, 'entmt_info/moviesingle_jy.html', content)
    return render(request, 'entmt_info/moviesingle.html', content)


# 검색 결과 페이지
def e_results(request):
    search_word = request.GET.get('search', '')
    result = api_python.api_search(search_word)

    # 장르 한글로 변경
    for i in range(len(result)):
        try:
            for j in range(len(result[i]['genre_ids'])):
                result[i]['genre_ids'][j] = Genres.objects.get(genre_id=result[i]['genre_ids'][j]).g_name
        except:
            print('---error---')

    result_comp = [{'res_id': res['id'], 'res_media_type': res['media_type']} for res in result]
    # res_rate = [Movies.objects.get(movie_id=int(res_id)).m_rateScore for res_id in result_id]
    result_rate = []
    for res_comp in result_comp:
        # if res_comp['res_media_type'] == 'movie':
        #     result_rate.append(Movies.objects.get(movie_id=int(res_comp['res_id'])).m_rateScore)
        # elif res_comp['res_media_type'] == 'tv':
        #     result_rate.append(Series.objects.get(series_id=int(res_comp['res_id'])).s_rateScore)
        # else: result_rate.append(0)
        if res_comp['res_media_type'] not in ['movie', 'tv']:
            result_rate.append(None)
        else:
            if res_comp['res_media_type'] == 'movie':
                try: result_rate.append(Movies.objects.get(movie_id=int(res_comp['res_id'])).m_rateScore)
                except: result_rate.append(0.0)
            else:
                try: result_rate.append(Series.objects.get(series_id=int(res_comp['res_id'])).s_rateScore)
                except: result_rate.append(0.0)

    print(f'result_rate={result_rate}')
    # print(result)
    for res, res_rate in zip(result, result_rate):
        res['rate'] = res_rate

    print(result)

    content = {
        'results': result,
    }

    # return render(request, 'entmt_info/results.html', content)
    return render(request, 'entmt_info/moviegrid.html', content)

# 댓글 등록
def submit_comment(request, media_id, media_type):
    # 현재 페이지 url
    url = request.META.get('HTTP_REFERER')

    # 테스트 프린트
    if media_type == 'movie':
        print(f'변경전 starRate : {Movies.objects.get(movie_id=media_id).m_rateScore}')
    elif media_type == 'tv':
        print(f'변경전 starRate : {Series.objects.get(series_id=media_id).s_rateScore}')


    if request.method == 'POST':
        # 기존 리뷰를 업데이트하는 경우
        if Mcomment.objects.filter(Q(mc_movie_id=media_id) & Q(mc_member=request.user)).exists():
            # filter에 객체가 존재하는 경우 업데이트
            comment = Mcomment.objects.filter(Q(mc_movie_id=media_id) & Q(mc_member=request.user))[0]
            form = McommentForm(request.POST, instance=comment)
            if form.is_valid():
                starRate(request.user.id, media_id, media_type, 'update', form.cleaned_data['mc_star'])
                form.save()
                messages.success(request, 'Your review has been updated!')
                return redirect(url)
            else:
                print('무효무효~!!')

        elif Scomment.objects.filter(Q(sc_series_id=media_id) & Q(sc_member=request.user)).exists():
            # filter에 객체가 존재하는 경우 업데이트
            comment = Scomment.objects.filter(Q(sc_series_id=media_id) & Q(sc_member=request.user))[0]
            form = ScommentForm(request.POST, instance=comment)

            if form.is_valid():
                starRate(request.user.id, media_id, media_type, 'update', form.cleaned_data['sc_star'])
                form.save()
                messages.success(request, 'Your review has been updated!')
                return redirect(url)
            else:
                print('무효무효~!!')

        # 새 리뷰를 등록하는 경우
        else:
            print('왜여기로와~~~')
            if media_type == 'movie':
                # 필터에 객체가 없는 경우 새로 등록
                form = McommentForm(request.POST)
                if form.is_valid():
                    user = Members.objects.get(pk=request.user.id)
                    movie = Movies.objects.get(pk=media_id)

                    data = Mcomment()
                    data.mc_title = form.cleaned_data['mc_title']
                    data.mc_star = form.cleaned_data['mc_star']
                    data.mc_content = form.cleaned_data['mc_content']
                    data.mc_movie = movie
                    data.mc_member = user
                    starRate(request.user.id, media_id, media_type, 'upload', data.mc_star)
                    data.save()
                    messages.success(request, 'Your review has been posted!')

                    return redirect(url)

            elif media_type == 'tv':
                # 필터에 객체가 없는 경우 새로 등록
                form = ScommentForm(request.POST)
                if form.is_valid():
                    user = Members.objects.get(pk=request.user.id)
                    series = Series.objects.get(pk=media_id)

                    data = Scomment()
                    data.sc_title = form.cleaned_data['sc_title']
                    data.sc_star = form.cleaned_data['sc_star']
                    data.sc_content = form.cleaned_data['sc_content']
                    data.sc_series = series
                    data.sc_member = user
                    starRate(request.user.id, media_id, media_type, 'upload', data.sc_star)
                    data.save()
                    messages.success(request, 'Your review has been posted!')

                    return redirect(url)

    else:
        print('get 방식으로 하셨나유? 코드작성 하셔유')

    # 테스트 프린트
    if media_type == 'movie':
        print(f'변경후 starRate : {Movies.objects.get(movie_id=media_id).m_rateScore}')
    elif media_type == 'tv':
        print(f'변경후 starRate : {Series.objects.get(series_id=media_id).s_rateScore}')




        # # 새 리뷰를 등록하는 경우
        # else:
        #     print('왜여기로와~~~')
        #     if media_type == 'movie':
        #         # 이미 리뷰가 존재하는 경우
        #         # 이거 없어도 될텐데,,,
        #         # if (Mcomment.objects.filter(mc_member=request.user)):
        #         if (Mcomment.objects.filter(Q(mc_movie_id=media_id) & Q(mc_member=request.user))):
        #             messages.error(request, '이미 리뷰를 등록하셨습니다!')
        #
        #             return redirect(url)
        #
        #         else:
        #             # 필터에 객체가 없는 경우 새로 등록
        #             form = McommentForm(request.POST)
        #             if form.is_valid():
        #                 user = Members.objects.get(pk=request.user.id)
        #                 movie = Movies.objects.get(pk=media_id)
        #
        #                 data = Mcomment()
        #                 data.mc_title = form.cleaned_data['mc_title']
        #                 data.mc_star = form.cleaned_data['mc_star']
        #                 data.mc_content = form.cleaned_data['mc_content']
        #                 data.mc_movie = movie
        #                 data.mc_member = user
        #                 starRate(request.user.id, media_id, media_type, 'upload', data.mc_star)
        #                 data.save()
        #                 messages.success(request, '리뷰가 등록되었습니다!')
        #
        #                 return redirect(url)
        #
        #             else:
        #                 messages.error(request, '오류!')
        #
        #     elif media_type == 'tv':
        #         # 이미 리뷰가 존재하는 경우
        #         if (Scomment.objects.filter(Q(sc_series_id=media_id) & Q(sc_member=request.user))):
        #             print('드라마 댓글 존재!!!')
        #             messages.error(request, '이미 리뷰를 등록하셨습니다!')
        #
        #             return redirect(url)
        #
        #         else:
        #             # 필터에 객체가 없는 경우 새로 등록
        #             form = ScommentForm(request.POST)
        #             if form.is_valid():
        #                 user = Members.objects.get(pk=request.user.id)
        #                 series = Series.objects.get(pk=media_id)
        #
        #                 data = Scomment()
        #                 data.sc_title = form.cleaned_data['sc_title']
        #                 data.sc_star = form.cleaned_data['sc_star']
        #                 data.sc_content = form.cleaned_data['sc_content']
        #                 data.sc_series = series
        #                 data.sc_member = user
        #                 starRate(request.user.id, media_id, media_type, 'upload', data.sc_star)
        #                 data.save()
        #                 messages.success(request, '리뷰가 등록되었습니다!')
        #
        #                 return redirect(url)
        #
        #             else:
        #                 messages.error(request, '오류!')




def delete_comment(request, comment_id, media_type):
    # 현재 url
    url = request.META.get('HTTP_REFERER')
    print('삭제 호출 ===')
    if request.user.is_authenticated:

        if media_type == 'movie':
            comment = get_object_or_404(Mcomment, pk=comment_id)
            media_id = comment.mc_movie_id
            # 로그인한 회원과 댓글 작성자가 같을 때만 삭제
            if comment.mc_member == request.user:
                starRate(request.user.id, media_id, media_type, 'delete', 0)
                comment.delete()
                print('삭제!!! ')
                messages.success(request, 'Your review has been deleted!')
                return redirect(url)

            # else:
            #     messages.error(request, 'ERROR')
            #     return redirect(url)

        elif media_type == 'tv':
            comment = get_object_or_404(Scomment, pk=comment_id)
            media_id = comment.sc_series_id
            # 로그인한 회원과 댓글 작성자가 같을 때만 삭제
            if comment.sc_member == request.user:
                starRate(request.user.id, media_id, media_type, 'delete', 0)
                comment.delete()
                messages.success(request, 'Your review has been deleted!')

                return redirect(url)

            # else:
            #     messages.error(request, 'ERROR')
            #     return redirect(url)

    else:
        return redirect('home')


def starRate(user_id, media_id, media_type, update_type, score):
    '''
    media_id : media_id
    score : 점수
    media_type : movie, tv 등 (Movies, Series 어떤거 쓸건지 정함)
    update_type : 0 - upload, 1 - update, 2 - delete

    comment_count : 현재등록된 comment 수
    upload 시 : (media.m_starRate*comment_count+score)/(comment_count+1)
    update 시 : (media.m_starRate*comment_count-원래등록되었던score+score)/comment_count
                =media.m_starRate + (-원래score+score)/comment_count
    delete 시 : (media.m_starRate*comment_count-원래score)/(comment_count-1)
    '''
    if media_type == 'movie':
        Media = Movies.objects.get(movie_id=media_id)
        media_star_rate = Media.m_rateScore
        try: ori_user_score = Mcomment.objects.get(Q(mc_movie_id=media_id) & Q(mc_member_id=user_id)).mc_star
        except: print('non_ori_user_score')
        comment_count = Mcomment.objects.filter(mc_movie_id=media_id).count()
        print(f'media_star_rate: {media_star_rate}')
        try: print(f'ori_user_score: {ori_user_score}')
        except: print('non_ori_user_score')
        print(f'comment_count: {comment_count}')
        if update_type == 'upload':
            update_score = ((media_star_rate * comment_count) + score) / (comment_count + 1)
            Media.m_rateScore = update_score
            Media.save()
        elif update_type == 'update':
            update_score = media_star_rate + ((score - ori_user_score) / comment_count)
            Media.m_rateScore = update_score
            Media.save()
        elif update_type == 'delete':
            if comment_count == 1:
                update_score = 0
            else:
                update_score = ((media_star_rate * comment_count) - ori_user_score) / (comment_count - 1)
            Media.m_rateScore = update_score
            Media.save()
        else: print('오류오류~')
        print(f'update_score: {update_score}')
    elif media_type == "tv":
        Media = Series.objects.get(series_id=media_id)
        media_star_rate = Media.s_rateScore
        try: ori_user_score = Scomment.objects.get(Q(sc_series_id=media_id) & Q(sc_member_id=user_id)).sc_star
        except: print('non_ori_user_score')
        comment_count = Scomment.objects.filter(sc_series_id=media_id).count()
        print(f'media_star_rate: {media_star_rate}')
        try: print(f'ori_user_score: {ori_user_score}')
        except: pass
        print(f'comment_count: {comment_count}')
        if update_type == 'upload':
            update_score = ((media_star_rate * comment_count) + score) / (comment_count + 1)
            Media.s_rateScore = update_score
            Media.save()
        elif update_type == 'update':
            update_score = media_star_rate + ((score - ori_user_score) / comment_count)
            Media.s_rateScore = update_score
            Media.save()
        elif update_type == 'delete':
            if comment_count == 1:
                update_score = 0
            else:
                update_score = ((media_star_rate * comment_count) - ori_user_score) / (comment_count - 1)
            Media.s_rateScore = update_score
            Media.save()
        else: print('오류오류~')
        print(f'update_score: {update_score} = {Series.objects.get(series_id=media_id).s_rateScore}')
    else: print('오류오류~')


