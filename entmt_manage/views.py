from django.shortcuts import render
from entmt_info.models import Movies, Series
from users.models import Mlike, Slike
# from django.contrib.auth import authenticate
from django.shortcuts import redirect
from django.db.models import Q


# Create your views here.
def em_like(request):
    if request.user.is_authenticated:
        results_id = request.GET.get('results_id', '')
        media_type = request.GET.get('media_type', '')
        user_id = request.user.id
        if media_type == 'movie':
            if Mlike.objects.filter(Q(ml_movie=results_id) & Q(ml_member=user_id)).exists():
                movie_like = Mlike.objects.get(Q(ml_movie=results_id) & Q(ml_member=user_id))
                movie_like.delete()
            else:
                Movie = Movies.objects.get(movie_id=results_id)
                movie_like = Mlike()
                movie_like.ml_member = request.user
                movie_like.ml_movie = Movie
                movie_like.save()
        elif media_type == 'tv':
            if Slike.objects.filter(Q(sl_series=results_id) & Q(sl_member=user_id)).exists():
                series_like = Slike.objects.get(Q(sl_series=results_id) & Q(sl_member=user_id))
                series_like.delete()
            else:
                # Series_ = Series.objects.get(series_id=results_id)
                series_like = Slike()
                series_like.sl_member_id = user_id
                series_like.sl_series_id = results_id
                series_like.save()
        else:
            print('구현되지 않았어요!')

    else:
        # 로그인 하세요 알림
        # 로그인하고나서 다시 원래있던 페이지로 돌아오게 해주세요!! 예)detail -> login -> detail
        print('와하하하')
        return redirect('users:login')
    # 구현해야함 : <tr onclick="location.href='/entmt_info/detail/?res_id={{ res.id }}&media_type={{ res.media_type }}'"
    redirect_url = '/entmt_info/detail/?res_id=' + str(results_id) + '&media_type=' + str(media_type)
    return redirect(redirect_url)
