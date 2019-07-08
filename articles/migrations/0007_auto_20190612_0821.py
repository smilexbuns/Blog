# Generated by Django 2.2.1 on 2019-06-12 08:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0006_auto_20190611_1943'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='content',
            field=models.TextField(default='', verbose_name='评论内容'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='avatar',
            field=models.ImageField(default='avatar/user/2019/06/default.jpg', upload_to='avatar/%Y/%m', verbose_name='头像'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='email',
            field=models.EmailField(max_length=50, verbose_name='邮箱'),
        ),
    ]
