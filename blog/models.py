from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from django.conf import settings


# Create your models here.
class PublishedManager(models.Manager):
	def get_queryset(self):
		return super(PublishedManager,self).get_queryset().filter(status='publish')

class Post(models.Model):
	STATUS_CHOICE= (
			('draft','Draft'),
			('publish','Publish'),
		)
	title = models.CharField(max_length=250)
	slug = models.SlugField(max_length=250, unique_for_date='publish')
	author = models.ForeignKey(User, on_delete=models.CASCADE,related_name='blog_post')
	body = models.TextField()
	publish = models.DateTimeField(default=timezone.now)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	status  = models.CharField(max_length=10, choices=STATUS_CHOICE,default='draft')

	likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='blog_likes', blank=True)

	objects = models.Manager()
	published = PublishedManager()

	def get_like_url(self):
		return reverse('blog:like_post', args=[self.slug])

	def get_blog_url(self):
		return reverse('blog:post_list')


	class Meta:
		ordering = ('-publish',)

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse('blog:detail',args=[self.slug])

class Comment(models.Model):
	post = models.ForeignKey(Post, on_delete=models.CASCADE,related_name='comments')
	name = models.CharField(max_length=80)
	email = models.EmailField()
	body = models.TextField()
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	active = models.BooleanField(default=True)

	comment_likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name = 'comment_likes',blank=True)

	class Meta:
		ordering = ('-created',)

	def __str__(self):
		return "Comment by {} on {}".format(self.name, self.post)

