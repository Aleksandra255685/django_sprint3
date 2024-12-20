from django.shortcuts import render, get_object_or_404
from django.http import Http404
from .models import Post, Category
from django.utils import timezone


def filter_posts():
    f_posts = (
        Post.objects.select_related(
            "category",
            "location",
            "author",
        )
        .filter(
            pub_date__lte=timezone.now(),
            is_published=True,
            category__is_published=True,
        )
    )
    return f_posts


def index(request):
    template_name = 'blog/index.html'
    context = {'post_list': filter_posts()[:5]}
    return render(request, template_name, context)


def post_detail(request, post_id):
    template_name = 'blog/detail.html'
    post = get_object_or_404(
        filter_posts(),
        pk=post_id,
    )
    context = {'post': post}
    return render(request, template_name, context)


def category_posts(request, category_slug):
    template_name = 'blog/category.html'
    category = get_object_or_404(
        Category,
        slug=category_slug,
        is_published=True
    )
    post_list = filter_posts().filter(category=category)
    context = {'category': category, 'post_list': post_list}
    return render(request, template_name, context)
