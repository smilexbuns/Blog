# _*_ encoding:utf-8 _*_
from django.db import models
from datetime import datetime
from mdeditor.fields import MDTextField

from users.models import UserProfile, UserFree
# Create your models here.


class Type(models.Model):
    name = models.CharField(verbose_name=u'分类名称', max_length=20)

    class Meta:
        verbose_name = u'分类'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(verbose_name=u'标签名称', max_length=20)

    class Meta:
        verbose_name = u'标签'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class ArticleManager(models.Manager):
    def distinct_date(self):
        distinct_date_list = []
        date_list = self.values('createtime').order_by('-createtime')
        for date in date_list:
            date = date['createtime'].strftime('%y')
            if date not in distinct_date_list:
                distinct_date_list.append(date)
        return distinct_date_list


class Article(models.Model):
    title = models.CharField(verbose_name=u'标题', max_length=50)
    type = models.ForeignKey(Type, verbose_name=u'文章类型', on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, verbose_name=u'文章标签')
    user = models.ForeignKey(UserProfile, verbose_name=u'作者', on_delete=models.CASCADE)
    desc = models.CharField(max_length=200, default='', verbose_name=u'概要')
    content = MDTextField(verbose_name=u'内容', default='')
    firstPicture = models.ImageField(verbose_name=u'首图', max_length=100, upload_to='picture/%Y/%m',)
    flag = models.CharField(verbose_name=u'标记', max_length=20, choices=((u'原创', u'原创'), (u'原创', u'转载'), (u'翻译', u'翻译')), default=u'原创')
    views = models.IntegerField(default=0, verbose_name=u'浏览次数')
    appreciate = models.IntegerField(default=0, verbose_name=u'赞赏次数')
    share = models.IntegerField(default=0, verbose_name=u'分享次数')
    published = models.BooleanField(verbose_name=u'是否发布', default=False)
    recommend = models.BooleanField(verbose_name=u'是否推荐', default=False)
    createtime = models.DateTimeField(verbose_name=u'创建时间', default=datetime.now)
    updatetime = models.DateTimeField(verbose_name=u'更新时间', default=datetime.now)
    objects = ArticleManager()

    class Meta:
        verbose_name = u'文章'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title


class UnPublishedArticle(Article):
    class Meta:
        verbose_name = u'待更文章'
        verbose_name_plural = verbose_name
        proxy = True


class Comment(models.Model):
    article = models.ForeignKey(Article, verbose_name=u'文章', on_delete=models.CASCADE)
    user = models.ForeignKey(UserFree, verbose_name=u'免费用户', default='', related_name='comments', on_delete=models.DO_NOTHING)
    root = models.ForeignKey('self', verbose_name=u'根评论', related_name='root_comment', null=True,blank=True, on_delete=models.DO_NOTHING)
    parent = models.ForeignKey('self', verbose_name=u'上级评论', related_name='parent_comment', null=True, blank=True, on_delete=models.CASCADE)
    reply_to = models.ForeignKey(UserFree, verbose_name=u'回复给', related_name='replies', null=True,blank=True, on_delete=models.DO_NOTHING)
    content = models.TextField(verbose_name=u'评论内容', default='')
    createtime = models.DateTimeField(verbose_name=u'评论时间', default=datetime.now)

    class Meta:
        verbose_name = u'评论'
        verbose_name_plural = verbose_name

