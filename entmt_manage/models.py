from django.db import models
from users.models import Members
from entmt_info.models import Movies, Series, Genres


class Mcomment(models.Model):
    mc_title = models.CharField(max_length=30, blank=False, default='')  # 댓글 제목
    mc_star = models.FloatField()    # 사용자가 설정한 별점
    mc_content = models.CharField(max_length=100, blank=True)    # 댓글 내용
    mc_member = models.ForeignKey(Members,
                              on_delete=models.CASCADE)    # 작성자
    mc_movie = models.ForeignKey(Movies,
                              on_delete=models.CASCADE)    # 작성한 영화
    mc_date = models.DateTimeField(auto_now=True)    # 댓글 작성 시간

    def __str__(self):
        return self.mc_title

class Scomment(models.Model):
    sc_title = models.CharField(max_length=30, blank=False, default='')  # 댓글 제목
    sc_star = models.FloatField()  # 사용자가 설정한 별점
    sc_content = models.CharField(max_length=255)    # 댓글 내용
    sc_member = models.ForeignKey(Members,
                              on_delete=models.CASCADE)    # 작성자
    sc_series = models.ForeignKey(Series,
                              on_delete=models.CASCADE)    # 작성한 드라마
    sc_date = models.DateTimeField(auto_now=True)    # 댓글 작성 시간


class Mgenres(models.Model):
    mg_movie = models.ForeignKey(Movies,
                              on_delete=models.CASCADE)
    mg_genre = models.ForeignKey(Genres,
                              on_delete=models.CASCADE)


class Sgenres(models.Model):
    sg_series = models.ForeignKey(Series,
                              on_delete=models.CASCADE)
    sg_genre = models.ForeignKey(Genres,
                              on_delete=models.CASCADE)
