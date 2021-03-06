# Generated by Django 2.2.1 on 2019-06-11 19:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0004_auto_20190610_2135'),
    ]

    operations = [
        migrations.CreateModel(
            name='UnPublishedArticle',
            fields=[
            ],
            options={
                'verbose_name': '待更文章',
                'verbose_name_plural': '待更文章',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('articles.article',),
        ),
        migrations.AlterModelOptions(
            name='article',
            options={'verbose_name': '已发文章', 'verbose_name_plural': '已发文章'},
        ),
        migrations.RemoveField(
            model_name='article',
            name='commentabled',
        ),
        migrations.RemoveField(
            model_name='article',
            name='sharestatement',
        ),
        migrations.AddField(
            model_name='article',
            name='share',
            field=models.IntegerField(default=0, verbose_name='分享次数'),
        ),
        migrations.AlterField(
            model_name='article',
            name='appreciate',
            field=models.IntegerField(default=0, verbose_name='赞赏次数'),
        ),
        migrations.AlterField(
            model_name='article',
            name='flag',
            field=models.CharField(choices=[('yc', '原创'), ('zz', '转载'), ('fy', '翻译')], default='原创', max_length=20, verbose_name='标记'),
        ),
    ]
