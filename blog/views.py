from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Post
from django.views.generic import ListView
from .forms import EmailPostForm
from django.core.mail import send_mail

def post_list(request):
	object_list = Post.objects.all()
	paginator = Paginator(object_list, 3)
	page = request.GET.get('page')
	try:
		posts = paginator.page(page)
	except PageNotAnInteger:
		# If page is not an integer, deliver the first page
		posts = paginator.page(1)
	except EmptyPage:
		# If page is out of range deliver last page of results
		posts = paginator.page(paginator.num_pages)
	return render(request, 'blog/post/list.html', {'posts': posts, 'page': page})

class PostListView(ListView):
	queryset = Post.objects.all()
	context_object_name = 'posts'
	paginate_by = 3
	template_name = 'blog/post/list.html'

def post_detail(request, year, month, day, post):
	post = get_object_or_404(Post, slug=post,
									publish__year=year,
									publish__month=month,
									publish__day=day)
	return render(request, 'blog/post/detail.html', {'post': post})

def post_share(request, post_id):
	#Retrieve post by id
	post = get_object_or_404(Post, id=post_id)
	sent = False
	form_class = EmailPostForm
	#^ If request is not POST, initialize an empty form
	form = form_class(request.POST or None)
	if request.method == 'POST':
		#Form was submitted
		form = EmailPostForm(request.POST)
		if form.is_valid():
			#Form fields passed validation
			cd = form.cleaned_data
			post_url = request.build_absolute_uri(post.get_absolute_url())
			subject = '{} ({}) recommends you read "{}"'.format(cd['name'], cd['email'], post.title)
			message = 'Read "{}" at {}\n\n{}\'s comments: {}'.format(post.title, post_url, cd['comments'])
			send_mail(subject, message, 'admin@myblog.com', [cd['to']])
			sent = True
		else:
			form = EmailPostForm()
	return render(request, 'blog/post/share.html', {'post': post,
													'form': form,
													'sent': sent})