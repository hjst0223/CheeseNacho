from django.contrib import admin
from entmt_info.models import Movies, Series, Genres

# Register your models here.
admin.site.register(Movies)
admin.site.register(Series)
admin.site.register(Genres)
