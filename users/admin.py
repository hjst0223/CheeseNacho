from django.contrib import admin
from users.models import Members, Mlike, Slike, Ugenres
# Register your models here.

admin.site.register(Members)
admin.site.register(Mlike)
admin.site.register(Slike)
admin.site.register(Ugenres)