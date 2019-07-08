# _*_ encoding:utf-8 _*_
"""Blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
import xadmin


from users.views import IndexView, TypesView, TagsView, ArcticleDetailView, PostCommentView, ArchiveView, SearchView

urlpatterns = [
    #后台管理
    path('admin/', admin.site.urls),
    # path('xadmin/', xadmin.site.urls),
    #首页
    path('', IndexView.as_view(), name='index'),
    #分类页
    path('types/', TypesView.as_view(), name='types'),
    #标签页
    path('tags/', TagsView.as_view(), name='tags'),
    #文章详情
    url(r'^article/(?P<article_id>\d+)/$', ArcticleDetailView.as_view(), name='article'),
    # 发表评论
    path('post_comment/<int:article_id>/', PostCommentView.as_view(), name='post_comment'),
    # #关于我
    # path('about/', AboutView.as_view(), name='about'),
    #归档
    url(r'^archives/$', ArchiveView.as_view(), name='archives'),
    #搜索
    url(r'^search/$', SearchView.as_view(), name='search'),
    #配置markdown
    url(r'mdeditor/', include('mdeditor.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)\
              + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
