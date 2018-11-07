from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.http import Http404, JsonResponse, HttpResponseRedirect, HttpResponse
from .models import Post, Comment
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView, RedirectView
from .forms import EmailPostForm, CommentForm, LikeForm, UploadBlogForm, UploadForm
from django.core.mail import send_mail
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required
def post_list(request):
	object_list = Post.published.all()
	paginator=Paginator(object_list,3)
	page = request.GET.get('page')
	try:
		posts=paginator.page(page)
	except PageNotAnInteger:
		posts = paginator.page(1)
	except EmptyPage:
		posts=paginator.page(paginator.num_pages)

	return render(request, 'blog/post/list.html',{'page':page,'posts':posts})

class PostListView(ListView):
	queryset = Post.published.all()
	context_object_name = 'posts'
	paginate_by = 3
	template_name = 'blog/post/list.html'


#def post_detail(request,slug):
#	post = get_object_or_404(Post, slug=slug,status = 'publish')
#	return render(request, 'blog/post/detail.html',{'post':post,'publish':publish,'slug':slug})


@login_required
def detail(request, slug):
	template_name = 'blog/post/detail.html'
	#post = Post.objects.get(slug=slug,status='publish')
	post = get_object_or_404(Post,slug=slug,status='publish')
	comment_form = CommentForm()
	likes = LikeForm()
	is_liked = False
	comments = post.comments.filter(active=True)
	
	if request.method == 'POST':
		comment_form = CommentForm(data=request.POST)
		likes = LikeForm(data=request.POST)
		if comment_form.is_valid():
			cf = comment_form.cleaned_data
			#new_comment = comment_form.save(commit=False)
			new_comment = Comment(post=post,name=cf['name'],email=cf['email'],body=cf['body'])
			new_comment.post = post
			new_comment.save()
			#return redirect(reverse('blog:detail'))
			return HttpResponseRedirect(post.get_absolute_url())

		else:
			comment_form = CommentForm()
	else:
		comment_form = CommentForm()
	return render(request, template_name, {'post':post,'slug':slug,'comments':comments,'comment_form':comment_form})

@login_required
def like_post(request):
	post = get_object_or_404(Post, slug=request.POST.get('post_id')) 
	is_liked = False
	if post.likes.filter(id=request.user.id).exists():
		post.likes.remove(request.user)
		is_liked = False
	else:
		post.likes.add(request.user)
		is_liked = True
	return HttpResponseRedirect(post.get_like_url())



@login_required
def post_share(request, post_id):
	form = EmailPostForm()
	post = get_object_or_404(Post, id=post_id, status='publish')
	sent=False
	if request.method == 'POST':
		form = EmailPostForm(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			post_url = request.build_absolute_uri(post.get_absolute_url())
			subject = '{} ({}) recommends you reading "{}"'.format(cd['name'],cd['email'],post.title)
			message = 'Read "{}" at {}\n\n{}\'s comments: {}'.format(post.title,post_url,cd['name'],cd['comments'])
			send_mail(subject, message, 'dengima2013@gmail.com',[cd['to']])
			sent = True
			return render(request, 'blog/post/share.html',{'post':post,'form':form,'sent':sent})
		else:
			return Http404()
	return render(request, 'blog/post/share.html',{'post':post,'form':form,'sent':sent})

@login_required
def posts_likes(self, slug):
	slug = self.kwargs.get('slug')
	print(slug) 
	obj = get_object_or_404(Post, slug=slug)
	url = obj.get_absolute_url()
	user = self.request.user
	if user.is_authenticated():
		obj.likes.remove(user)
	else:
		obj.likes.add(user)
	return url_



#class PostLikeToggle(RedirectView):
#	def get_redirect_url(self, *args, **kwargs):
#		slug = self.kwargs.get('slug')
#		print(slug)
#		obj = get_object_or_404(Post, *args, **kwargs)
#		url = obj.get_absolute_url()
#		user = self.request.user
#		if user.is_authenticated():
#			obj.likes.remove(user)
#		else:
#			obj.likes.add(user)
#		return url_

@login_required
def blog_post(request):
	blog_forms = UploadBlogForm()
	if request.method == "POST":
		blog_forms = UploadBlogForm(request.POST)
		if blog_forms.is_valid():
			blg = blog_forms.cleaned_data
			new_blog = Post(title=blg['title'],slug=blg['title'],body=blg['body'],author=request.user)
			new_blog.save()
			return redirect(reverse('dashboard'))
		else:
			blog_forms = UploadBlogForm()
			return render(request, 'blog/post/blog_upload.html',{'blog_forms':blog_forms})
	else:
		blog_forms = UploadBlogForm()
		return render(request, 'blog/post/blog_upload.html',{'blog_forms':blog_forms})
	return render(request, 'blog/post/blog_upload.html',{'blog_forms':blog_forms})