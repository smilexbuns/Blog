from django.contrib import admin
from .models import UserProfile, UserFree
# Register your models here.


class UserFreeAdmin(admin.ModelAdmin):
    list_display = ['nickname', 'email']
    search_fields = ['nickname', 'email']
    list_per_page = 10
    list_filter = ['nickname', 'email']


admin.site.register(UserProfile)
admin.site.register(UserFree, UserFreeAdmin)