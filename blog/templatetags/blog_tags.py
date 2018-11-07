from django import template
from django.db.models import Count
from django.utils.safestring import mark_safe


register = template.Library()

from ..models import Post

#Number of blogs posted
@register.simple_tag
def total_posts():
	return Post.published.count()

#recently posted blogs
@register.inclusion_tag('blog/post/latest_posts.html')
def show_latest_posts(count=5):
	latest_posts = Post.published.order_by('-publish')[:count]
	return {'latest_posts':latest_posts}

#Displays most commented or liked posts
@register.simple_tag
def get_most_commented_posts(count=3):
	return Post.published.annotate(total_comments=Count('comments')).order_by('-total_comments')[:count]

