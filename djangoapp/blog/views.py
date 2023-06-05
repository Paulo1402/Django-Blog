from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404

from blog.models import Post, Page


def index(request):
    posts = Post.objects.get_published()

    paginator = Paginator(posts, 9)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        'blog/pages/index.html',
        {
            'page_obj': page_obj,
        }
    )


def created_by(request, author_id: int):
    posts = Post.objects.get_published().filter(created_by_id=author_id)

    paginator = Paginator(posts, 9)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        'blog/pages/index.html',
        {
            'page_obj': page_obj,
        }
    )


def category(request, slug: str):
    posts = Post.objects.get_published().filter(category__slug=slug)

    paginator = Paginator(posts, 9)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        'blog/pages/index.html',
        {
            'page_obj': page_obj,
        }
    )


def page(request, slug: str):
    page = get_object_or_404(Page, slug=slug, is_published=True)

    return render(
        request,
        'blog/pages/page.html',
        {
            'page': page,
        }
    )


def post(request, slug: str):
    post = get_object_or_404(Post, slug=slug, is_published=True)

    return render(
        request,
        'blog/pages/post.html',
        {
            'post': post
        }
    )
