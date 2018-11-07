from . import views
from django.urls import path

app_name = 'blog'

urlpatterns=[
	path('blog_upload/', views.blog_post, name='blog_post'),
	#path('', views.post_list, name='post_list'),
	path('', views.PostListView.as_view(), name='post_list'),
	#path('<str:slug>/', views.post_detail, name='post_detail'), 
	path('<str:slug>/', views.detail, name='detail'),
	path('<int:post_id>/share/', views.post_share, name='post_share'),
	path('<str:slug>/', views.like_post, name='like_post'),

]
