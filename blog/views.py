from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout
from django.urls import reverse_lazy
from django.http import HttpResponse,JsonResponse
from django.contrib.auth.models import User
from .models import ArticlePost,Comment,User_Info
from django.core.paginator import Paginator
from .forms import UserLoginForm,UserRegisterForm,User_detailForm
from django.views import View

# Create your views here.
def article_list(request):
    # 根据get请求的查询条件返回
    if request.GET.get('order')=="total_views":
        article_list= ArticlePost.objects.order_by('-total_views')
        order='total_view'
    else:
        article_list=ArticlePost.objects.all()
        order='normal'
    paginater=Paginator(article_list,4)
    page=request.GET.get('page')
    articles=paginater.get_page(page)
    context={'articles':articles,'order':order}
    return render(request,'article/list.html',context)

@login_required(login_url=reverse_lazy('blog:user_login'))
def article_create(request):
    if request.method=='POST':
        title,body,author=request.POST.get('title'),request.POST.get('body'),request.user
        ArticlePost.objects.create(title=title,body=body,author=author)
        return redirect('blog:article_list')
    else:
        return render(request,'article/create.html')
# 详情
def article_detail(request,id):
    # article=ArticlePost.objects.get(id=id)
    article=get_object_or_404(ArticlePost,id=id)
    article.total_views+=1
    article.save(update_fields=['total_views'])
    # article.update(total_views=F('total_views')+1)
    comments=Comment.objects.filter(article=id)
    return render(request,'article/detail.html',{'article':article,'comments':comments})

def article_delete(request,id):
    article=ArticlePost.objects.get(id=id)
    article.delete()
    return redirect('blog:article_list')

# 更新
@login_required(login_url=reverse_lazy('blog:user_login'))
def article_update(request,id):
    article=ArticlePost.objects.get(id=id)
    if request.user!=article.author:
        return HttpResponse('您无权限删除此文章')
    if request.method=='POST':
        article.title,article.body=request.POST.get('title'),request.POST.get('body')
        article.save()
        return redirect('blog:article_detail',id=id)
    else:
        return render(request,'article/update.html',{'article':article})

# 评论
# @login_required(login_url='/userprofile/login/')
# def post_comment(request,article_id):
#     article=get_object_or_404(ArticlePost,id=article_id)
#     # print(request,request.user,request.POST)
#     if request.method=='POST':
#         body,user,pid=request.POST.get('body').strip(),request.user,request.POST.get('pid')
#         if body:
#             Comment.objects.create(article=article,body=body,user=user,pre_comment_id=pid)
#         return redirect('blog:article_detail',id=article_id)
#     else:
#         return HttpResponse('评论只接受POST请求')

# 评论后改为返回json
@login_required(login_url='/userprofile/login/')
def post_comment(request,article_id):
    article=get_object_or_404(ArticlePost,id=article_id)
    # print(request,request.user,request.POST)
    if request.method=='POST':
        body,user,pid=request.POST.get('body').strip(),request.user,request.POST.get('pid')
        if body:
            Comment.objects.create(article=article,body=body,user=user,pre_comment_id=pid)
        comment=list(Comment.objects.filter(article=article).values('id','article_id','user'))
        return JsonResponse(comment,safe=False)
    else:
        return HttpResponse('评论只接受POST请求')

# 用户
def user_login(request):
    if request.method=='POST':
        user_login_form=UserLoginForm(data=request.POST)
        if user_login_form.is_valid():
            data=user_login_form.cleaned_data
            user=authenticate(username=data['username'],password=data['password'])
            if user:
                login(request,user)
                return redirect('blog:article_list')
            else:
                return HttpResponse('用户名或密码输入有误，请重新输入')
        else:
            return HttpResponse('用户名或密码输入不合法')
    elif request.method=='GET':
        return render(request,'userprofile/login.html',{'form':UserLoginForm()})

def user_logout(request):
    logout(request)
    return redirect('blog:article_list')

def user_register(request):
    if request.method=='POST':
        user_register_form=UserRegisterForm(data=request.POST)
        # print(request.POST,user_register_form.errors)
        if user_register_form.is_valid():
            user=user_register_form.save(commit=False)
            user.set_password(user_register_form.cleaned_data['password'])
            user.save()
            User_Info.objects.create(user=user)
            login(request,user)
            return redirect('blog:article_list')
        else:
            return HttpResponse('输入有误，请重新输入')
    elif request.method=='GET':
        return render(request,'userprofile/register.html',{'form':UserRegisterForm()})
    else:
        return HttpResponse('请使用GET或POST请求数据')

def user_detail(request,user_id):
    show_user=get_object_or_404(User,id=user_id)
    show_user_info=get_object_or_404(User_Info,user=show_user)
    show_user_form=User_detailForm(instance=show_user_info)
    return render(request,'userprofile/detail.html',locals())