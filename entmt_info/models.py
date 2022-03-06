from django.db import models


class Movies(models.Model):
    movie_id = models.IntegerField(primary_key=True)   # 영화 id
    m_title = models.CharField(max_length=255)    # 영화 제목
    m_posterPath = models.CharField(max_length=50)   # 포스터 path
    m_likeCount = models.IntegerField(default=0)    # 찜 수
    m_releaseDate = models.DateField()    # 개봉일
    m_popularity = models.FloatField()    # 인기도

    def __str__(self):
        return self.m_title

    # def avg_rating(self):
    #     sum = 0
    #     ratings = Mcomment.objects.filter(movies=self)
    #     for rating in ratings:
    #         sum += rating.mc_star
    #
    #     if len(ratings) > 0:
    #         return sum / len(ratings)
    #     else:
    #         return 0


class Series(models.Model):
    series_id = models.IntegerField(primary_key=True)   # 드라마 id
    s_title = models.CharField(max_length=255)    # 드라마 제목
    s_posterPath = models.CharField(max_length=50)   # 포스터 path
    s_likeCount = models.IntegerField(default=0)    # 찜 수
    s_firstAirDate = models.DateField()    # 첫 방영일
    s_lastAirDate = models.DateField()    # 마지막 방영일
    s_popularity = models.FloatField()    # 인기도

    def __str__(self):
        return self.s_title


class Genres(models.Model):
    genre_id = models.IntegerField(primary_key=True)    # 장르 id
    g_name = models.CharField(max_length=30)   # 장르명

    def __str__(self):
        return self.g_name
