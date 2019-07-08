# _*_ encoding:utf-8 _*_
from django.db import models
from datetime import datetime
from django.contrib.auth.models import AbstractUser
# Create your models here.


class UserProfile(AbstractUser):
    nickname = models.CharField(max_length=50, verbose_name=u'昵称', default='')
    email = models.EmailField(verbose_name=u'邮箱', max_length=50)
    avatar = models.ImageField(upload_to='avatar/user/%Y/%m', default=u'image/default.png', verbose_name=u'头像', max_length=100)
    createtime = models.DateTimeField(verbose_name=u'创建时间', default=datetime.now)
    updatetime = models.DateTimeField(verbose_name=u'更新时间', default=datetime.now)

    class Meta:
        verbose_name = u'用户'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username


class UserFree(models.Model):
    nickname = models.CharField(verbose_name=u'昵称', max_length=20)
    email = models.EmailField(verbose_name=u'邮箱', max_length=50)
    avatar = models.ImageField(upload_to='avatar/%Y/%m', default=u'avatar/user/2019/06/default.jpg', verbose_name=u'头像',
                               max_length=100)

    class Meta:
        verbose_name = u'免费用户'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.nickname