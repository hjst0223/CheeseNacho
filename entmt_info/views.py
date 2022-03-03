from django.shortcuts import render, get_object_or_404
from entmt_info.models import Movies, Series
from entmt_info.forms import MoviesDetailForm, SeriesDetailForm


# 상세 정보 페이지
def e_detail(request, movie_id, series_id):
    # ModelForm을 이용해서 Database에서 가져온 내용을 화면에 출력
    # movie_id와 series_id로 이용해서 영화, 시리즈 객체 가져오기
    movies = get_object_or_404(Movies, pk=movie_id)
    series = get_object_or_404(Series, pk=series_id)

    # EntmtDetailForm이라는 ModelForm의 객체를
    # 위에서 만든 Movies와 Series class의 객체를 이용하여 각각 생성하기
    movie_detail_form = MoviesDetailForm(instance=movies)
    series_detail_form = SeriesDetailForm(instance=series)

    # 댓글 정보 가져오기
    m_comments = movies.comment_set.all().order_by('mc_date')
    s_comments = series.comment_set.all().order_by('sc_date')

    context = {
        "movie_detail_form": movie_detail_form,
        "series_detail_form": series_detail_form,
        'm_comments': m_comments,
        's_comments': s_comments
    }

    return render(request, 'entmt_info/detail.html')


# 검색 결과 페이지
def e_results(request):

    return render(request, 'entmt_info/results.html')
