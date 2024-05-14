from django.shortcuts import get_object_or_404, render
from django.http import Http404
from .models import Post, Category
from django.utils import timezone


def index(request):
    post_list = Post.objects.all().filter(
        is_published=True,
        category__is_published=True,
        pub_date__lte=timezone.now()).order_by('-created_at',)[:5]
    return render(request, 'blog/index.html',
                  {'post_list': post_list})


def post_detail(request, post_id):
    post = get_object_or_404(Post.objects.all().filter(
        id=post_id,
        is_published=True,
        category__is_published=True,
        pub_date__lte=timezone.now()))
    context = {'post': post}
    if post:
        return render(request, 'blog/detail.html', context)
    raise Http404('Post does not exist')


def category_posts(request, category_slug):
    category = get_object_or_404(Category,
                                 slug=category_slug,
                                 is_published=True)
    post_list = Post.objects.select_related('category', 'location').filter(
        is_published=True,
        category__slug=category_slug,
        category__is_published=True,
        pub_date__lte=timezone.now())
    context = {
        'category': category,
        'post_list': post_list
    }
    if post_list and category:
        return render(request, 'blog/category.html', context)
    raise Http404('Post does not exist')
