from django import template
from django.db.models import Count

register = template.Library()

from ..models import Post

@register.simple_tag
def post_count():
	return Post.objects.count()

@register.inclusion_tag('blog/post/latest_posts.html')
def show_latest_posts(count=5):
	latest_posts = Post.objects.order_by('-created')[:count]
	return {'latest_posts': latest_posts}

@register.assignment_tag
def get_most_commented_posts(count=5):
	return Post.published.annotate(total_comments=Count('comments')).order_by('-total_comments')[:count]