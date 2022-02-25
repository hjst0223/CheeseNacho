from django.contrib import admin
from entmt_manage.models import Mcomment, Scomment, Mgenres, Sgenres

# Register your models here.
admin.site.register(Mcomment)
admin.site.register(Scomment)
admin.site.register(Mgenres)
admin.site.register(Sgenres)


