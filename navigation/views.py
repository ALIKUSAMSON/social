from django.shortcuts import render

# Create your views here.
def index(request):
	template = 'navigation/index.html'
	context = locals()
	return render(request, template, context)

def contact(request):
	template = 'navigation/contact.html'
	context = locals()

	return render(request, template, context)

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