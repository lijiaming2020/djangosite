# Generated by Django 3.2.9 on 2022-02-08 08:22

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ('-created',), 'verbose_name': '评论', 'verbose_name_plural': '评论'},
        ),
        migrations.CreateModel(
            name='User_Info',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img', models.ImageField(blank=True, upload_to='image/user/%Y/%m/%d/', verbose_name='头像')),
                ('phone', models.PositiveIntegerField(blank=True, verbose_name='手机号码')),
                ('address', models.CharField(blank=True, max_length=200, verbose_name='地址')),
                ('conditon', models.CharField(blank=True, default='无', max_length=20, verbose_name='心情状态')),
                ('birthday', models.DateField(default=datetime.datetime(2002, 2, 13, 8, 22, 5, 466124, tzinfo=utc), verbose_name='生日')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='user_info', to=settings.AUTH_USER_MODEL, verbose_name='账号')),
            ],
            options={
                'verbose_name': '个人主页信息',
                'verbose_name_plural': '个人主页信息',
            },
        ),
    ]
