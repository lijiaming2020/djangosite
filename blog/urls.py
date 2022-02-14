from django.urls import path
from . import views as blogviews
from django.conf.urls import url

app_name='blog'
urlpatterns = [
    url(r'^$', blogviews.article_list),
    path('article_list/', blogviews.article_list,name='article_list'),
    path('article_create/', blogviews.article_create, name='article_create'),
    path('article_detail/<int:id>/', blogviews.article_detail, name='article_detail'),
    path('article_delete/<int:id>/', blogviews.article_delete, name='article_delete'),
    path('article_update/<int:id>/', blogviews.article_update, name='article_update'),

    path('post_comment/<int:article_id>/', blogviews.post_comment, name='post_comment'),

    path('user_login/', blogviews.user_login, name='user_login'),
    path('user_logout/', blogviews.user_logout, name='user_logout'),
    path('user_register/', blogviews.user_register, name='user_register'),
    path('user_info/<int:user_id>/', blogviews.user_detail, name='user_detail'),
]