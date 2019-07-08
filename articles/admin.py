from django.contrib import admin
from .models import Article, Tag, Type, Comment, UnPublishedArticle


class AritcleAdmin(admin.ModelAdmin):
    list_display = ['title', 'type', 'user', 'firstPicture', 'flag', 'published', 'recommend', 'createtime', 'updatetime']
    search_fields = ['title', 'type', 'tags', 'user', 'flag']
    list_filter = ['title', 'type', 'tags', 'user', 'flag', 'createtime', 'updatetime']
    exclude = ['views', 'createtime', 'updatetime', 'share', 'appreciate']
    list_editable = [ 'published', 'recommend', 'createtime', 'updatetime', 'firstPicture']
    list_per_page = 10

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.filter(published=True)
        return qs


class UnPublishedAritcleAdmin(admin.ModelAdmin):
    list_display = ['title', 'type', 'user', 'flag', 'published', 'recommend', 'createtime', 'updatetime']
    search_fields = ['title', 'type', 'tags', 'user', 'flag']
    list_filter = ['title', 'type', 'tags', 'user', 'flag', 'createtime', 'updatetime']
    exclude = ['views', 'createtime', 'updatetime', 'share', 'appreciate']
    list_editable = ['published', 'recommend']
    list_per_page = 10

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.filter(published=False)
        return qs


class TagAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']
    list_per_page = 10
    list_filter = ['name']


class TypeAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']
    list_per_page = 10
    list_filter = ['name']


admin.site.register(Article, AritcleAdmin)
admin.site.register(UnPublishedArticle, UnPublishedAritcleAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Type, TypeAdmin)
admin.site.register(Comment)
admin.AdminSite.site_header ='博客管理后台'
admin.AdminSite.site_title = '博客系统'