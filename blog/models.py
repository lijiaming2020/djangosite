from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta

# Create your models here.

class ArticlePost(models.Model):
    """
    文章
    """
    author=models.ForeignKey(User,verbose_name='作者',on_delete=models.CASCADE)
    title=models.CharField(verbose_name='标题',max_length=100)
    body=models.TextField(verbose_name='内瑞')
    created=models.DateTimeField(verbose_name='创建时间',default=timezone.now)
    updated=models.DateTimeField(verbose_name='更新时间',auto_now=True)
    total_views=models.PositiveIntegerField(verbose_name='点击量',default=0)
    class Meta:
        ordering=('-created',)
        verbose_name=verbose_name_plural='文章'
    def __str__(self):
        return f'{self.title}'

class Comment(models.Model):
    """
    文章评论
    """
    article=models.ForeignKey(ArticlePost,verbose_name='文章',on_delete=models.DO_NOTHING,related_name='comments')
    user=models.ForeignKey(User,verbose_name='发表人',on_delete=models.CASCADE,related_name='comments')
    body=models.TextField(verbose_name='内瑞',blank=False)
    pre_comment=models.ForeignKey('self',on_delete=models.DO_NOTHING,verbose_name='原评论',null=True)
    created=models.DateTimeField(verbose_name='创建时间',auto_now_add=True)
    class Meta:
        ordering=('-created',)
        verbose_name=verbose_name_plural='评论'
    def __str__(self):
        return f'{self.body[:20]}'

class User_Info(models.Model):
    """
    个人首页信息
    """
    user=models.OneToOneField(User,verbose_name='账号',on_delete=models.CASCADE,related_name='user_info')
    img=models.ImageField(upload_to='image/user/%Y/%m/%d/',verbose_name='头像',default='image/user/default.png')
    phone=models.PositiveIntegerField(verbose_name='手机号码',blank=True,null=True)
    address=models.CharField(verbose_name='地址',max_length=200,blank=True)
    conditon=models.CharField(verbose_name='心情状态',max_length=20,blank=True,default='无')
    birthday=models.DateField(verbose_name='生日',default=timezone.now().date()-timedelta(days=20*365))
    class Meta:
        verbose_name=verbose_name_plural='个人主页信息'
    def __str__(self):
        return f'{self.user}'
    def get_age(self):
        return int((timezone.now().date()-self.birthday).days//365.25)
