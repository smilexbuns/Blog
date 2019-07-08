# Generated by Django 2.2.1 on 2019-06-12 15:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_remove_userprofile_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserFree',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nickname', models.CharField(max_length=20, verbose_name='昵称')),
                ('email', models.EmailField(max_length=50, verbose_name='邮箱')),
                ('avatar', models.ImageField(default='avatar/user/2019/06/default.jpg', upload_to='avatar/%Y/%m', verbose_name='头像')),
            ],
        ),
    ]
