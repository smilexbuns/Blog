# Generated by Django 2.2.1 on 2019-06-12 16:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_userfree'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='userfree',
            options={'verbose_name': '免费用户', 'verbose_name_plural': '免费用户'},
        ),
    ]
