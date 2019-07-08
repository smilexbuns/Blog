import markdown
from django.shortcuts import render
from django.views import View
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from django.db.models import Q
import json
from markdown.extensions.toc import TocExtension
from django.utils.text import slugify
from collections import defaultdict
import requests

from articles.models import Article, Type, Tag, Comment
# Create your views here.
from users.models import UserFree


class IndexView(View):
    """首页"""
    def get(self, request):
        # 通过ip地址查询所在地区
        ip_url = 'http://fangyuanxiaozhan.com/get_ip'
        default_urldata = requests.get(ip_url).json()
        default_ip = default_urldata['ip']
        city_url = 'http://ip.taobao.com/service/getIpInfo.php?ip={}'.format(default_ip)
        default_data = requests.get(city_url).json()
        default_city = default_data['data']['city']
        print(default_city)
        url = 'http://wthrcdn.etouch.cn/weather_mini?city={}'.format(default_city)
        json_data = requests.get(url).json()
        status = json_data['status']
        weather = json_data['data']['forecast']
        tip = json_data['data']['ganmao']
        today_weather = weather[0]
        city = json_data['data']['city']
        #获取文章
        types = Type.objects.all()
        tags = Tag.objects.all()
        all_articles = Article.objects.filter(published=True)
        type_id = request.GET.get('type', '')
        if type_id:
            all_articles = all_articles.filter(type_id=int(type_id))
        tag_id = request.GET.get('tag', '')
        if tag_id:
            tag = Tag.objects.get(id=int(tag_id))
            all_articles = tag.article_set.all()
        articles_nums = all_articles.count()
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_articles, 9, request=request)

        articles = p.page(page)

        types = Type.objects.all()[:6]
        tags = Tag.objects.all()[:4]
        new_articles = Article.objects.filter(recommend=True).order_by('-createtime')[:3]
        hot_articles = Article.objects.filter(recommend=True).order_by('-views')[:3]
        return render(request, 'index.html', {
            'types': types,
            'tags': tags,
            'articles': articles,
            'new_articles': new_articles,
            'hot_articles': hot_articles,
            'article_nums': articles_nums,
            'today': today_weather,
            'city': city,
            'tip': tip
        })


class TypesView(View):
    """分类"""
    def get(self, request):
        types = Type.objects.all()
        tags = Tag.objects.all()[:5]
        all_articles = Article.objects.filter(published=True)
        type_id = request.GET.get('type', '')
        if type_id:
            all_articles = all_articles.filter(type_id=int(type_id))
        articles_nums = all_articles.count()
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_articles, 9, request=request)

        articles = p.page(page)

        new_articles = Article.objects.filter(recommend=True).order_by('-createtime')[:3]
        hot_articles = Article.objects.filter(recommend=True).order_by('-views')[:3]
        return render(request, 'types.html', {
            'types': types,
            'articles': articles,
            'new_articles': new_articles,
            'hot_articles': hot_articles,
            'article_nums': articles_nums,
            'tags': tags
        })


class TagsView(View):
    """标签"""
    def get(self, request):
        types = Type.objects.all()[:5]
        tags = Tag.objects.all()
        all_articles = Article.objects.filter(published=True)
        tag_id = request.GET.get('tag', '')
        if tag_id:
            tag = Tag.objects.get(id=int(tag_id))
            all_articles = tag.article_set.all()
        articles_nums = all_articles.count()
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_articles, 9, request=request)

        articles = p.page(page)

        new_articles = Article.objects.filter(recommend=True).order_by('-createtime')[:3]
        hot_articles = Article.objects.filter(recommend=True).order_by('-views')[:3]
        return render(request, 'tags.html', {
            'tags': tags,
            'articles': articles,
            'new_articles': new_articles,
            'hot_articles': hot_articles,
            'article_nums': articles_nums,
            'types': types
        })


class ArcticleDetailView(View):
    """文章详情"""
    def get(self, request, article_id):
        types = Type.objects.all()[:5]
        article = Article.objects.get(id=int(article_id))
        related_articles = Article.objects.filter(type=article.type)[:12]
        tags = article.tags.all()
        comments = Comment.objects.filter(article_id=int(article_id), parent=None)
        article.views += 1
        article.save()

        md = markdown.Markdown(
            extensions=[
                'markdown.extensions.extra',
                'markdown.extensions.codehilite',
                # 目录扩展
                TocExtension(slugify=slugify),
            ]
        )
        article.content = md.convert(article.content)
        return render(request, 'blogs.html', {
            'article': article,
            'toc': md.toc,
            'comments': comments,
            'related_articles': related_articles,
            'tags': tags,
            'types': types
        })


class PostCommentView(View):
    """评论和回复"""
    def post(self, request, article_id):
        comment = Comment()
        user = UserFree()
        content = request.POST.get('content', '')
        nickname = request.POST.get('nickname', '')
        email = request.POST.get('email', '')
        if nickname == '' or email == '':
            user.nickname = '匿名用户'
            user.email = ''
        else:
            user.nickname = nickname
            user.email = email
        user.save()
        reply_comment_id = request.POST.get('reply_comment_id')
        if int(reply_comment_id) < 0:
            return HttpResponse('{"status":"fail", "msg":"回复出错"}', content_type='application/json')
        elif int(reply_comment_id) == 0:
            comment.parent = None
            comment.root = None
            comment.article_id = article_id
            comment.content = content
            comment.user = user
            comment.save()
            return HttpResponse('{"status":"success", "msg":"评论成功"}', content_type='application/json')
        elif int(reply_comment_id) > 0:
            parent = Comment.objects.get(id=int(reply_comment_id))
            if parent:
                if parent.root is None:
                    comment.root_id = parent.id
                else:
                    comment.root_id = parent.root_id
                comment.article_id = article_id
                comment.parent = parent
                comment.content = content
                comment.reply_to = parent.user
                comment.user = user
                comment.save()
                return HttpResponse('{"status":"success", "msg":"回复成功"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail", "msg":"回复出错"}', content_type='application/json')


# class AboutView(View):
#     """关于我"""
#     def get(self, request):
#         return render(request, 'about.html', {})


class ArchiveView(View):
    """归档"""
    def get(self, request):
        types = Type.objects.all()[:5]
        archive_list = Article.objects.distinct_date()
        # print(archive_list)
        # for year in archive_list:
        #     print(year)
        #     article_list = Article.objects.filter(createtime__year=year).values()
        #     print(article_list)
        #     archives[year].append(article_list)
        # print(archives[1])
        article_list = Article.objects.all().order_by('-createtime')
        new_articles = article_list[:3]
        return render(request, 'archive.html', {
            'new_articles': new_articles,
            'types': types,
            'article_list': article_list
        })


class SearchView(View):
    def get(self, request):
        # search_keywords = req['keywords'] if 'keywords' in req else ''
        search_keywords = request.GET.get('keywords', '')
        all_articles = Article.objects.all()
        if search_keywords:
            all_articles = all_articles.filter(
                Q(title__icontains=search_keywords) | Q(desc__icontains=search_keywords))
        #Q(tags__name__icontains=search_keywords) | Q(type__name__icontains=search_keywords)
        articles_nums = all_articles.count()
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_articles, 9, request=request)

        articles = p.page(page)
        return render(request, 'search.html', {
            'search_list': articles,
            'search_number': articles_nums
        })


# def page_not_found(request, **kwargs):
#     #全局404
#     response = render('404.html', {})
#     response.status_code = 404
#     return response
#
#
# def page_error(request, **kwargs):
#     #全局500
#     response = render('500.html', {})
#     response.status_code = 500
#     return response