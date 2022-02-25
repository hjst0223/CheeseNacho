from django.db import models

class Movies(models.Model):
    movie_id = models.IntegerField(primary_key=True)   # 영화 id
    m_title = models.CharField(max_length=255)    # 영화 제목
    m_posterPath = models.CharField(max_length=50)   # 포스터 path
    m_likeCount = models.IntegerField(default=0)    # 찜 수
    m_releaseDate = models.DateField()    # 개봉일

    def __str__(self):
        return self.m_title


class Series(models.Model):
    series_id = models.IntegerField(primary_key=True)   # 드라마 id
    s_title = models.CharField(max_length=255)    # 드라마 제목
    s_posterPath = models.CharField(max_length=50)   # 포스터 path
    s_likeCount = models.IntegerField(default=0)    # 찜 수
    s_firstAirDate = models.DateField()    # 첫 방영일
    s_lastAirDate = models.DateField()    # 마지막 방영일

    def __str__(self):
        return self.s_title

class Genres(models.Model):
    genre_id = models.IntegerField(primary_key=True)    # 장르 id
    g_name = models.CharField(max_length=30)   # 장르명
#
#
# class Mcomment(models.Model):
#     mc_star = models.IntegerField(default=0)    # 별점
#     mc_content = models.CharField(max_length=100)    # 댓글 내용
#     mc_member = models.ForeignKey(Members,
#                               on_delete=models.CASCADE)    # 작성자
#     mc_movie = models.ForeignKey(Movies,
#                               on_delete=models.CASCADE)    # 작성한 영화
#     mc_date = models.DateTimeField(auto_now=True)    # 댓글 작성 시간
#
#
# class Scomment(models.Model):
#     sc_star = models.IntegerField(default=0)    # 별점
#     sc_content = models.CharField(max_length=255)    # 댓글 내용
#     sc_member = models.ForeignKey(Members,
#                               on_delete=models.CASCADE)    # 작성자
#     sc_series = models.ForeignKey(Series,
#                               on_delete=models.CASCADE)    # 작성한 드라마
#     sc_date = models.DateTimeField(auto_now=True)    # 댓글 작성 시간
#
#
# class Mgenres(models.Model):
#     mg_movie = models.ForeignKey(Movies,
#                               on_delete=models.CASCADE)
#     mg_genre = models.ForeignKey(Genres,
#                               on_delete=models.CASCADE)
#
#
# class Sgenres(models.Model):
#     sg_series = models.ForeignKey(Series,
#                               on_delete=models.CASCADE)
#     sg_genre = models.ForeignKey(Genres,
#                               on_delete=models.CASCADE)
