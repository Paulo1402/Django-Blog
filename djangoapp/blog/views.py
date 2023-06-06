from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.views.generic.list import ListView

from blog.models import Post, Page

PER_PAGE = 9


class BaseListView(ListView):
    """Base class para templates usando index.html"""

    template_name = 'blog/pages/index.html'
    paginate_by = PER_PAGE
    queryset = Post.objects.get_published()
    allow_empty = True


class IndexListView(BaseListView):
    """View para home"""

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context.update({
            'page_title': 'Home - ',
        })

        return context


class SearchListView(BaseListView):
    """View para pesquisas usando o campo de pesquisa"""

    def __init__(self):
        super().__init__()
        self._search_value = ''

    def get_queryset(self):
        self._search_value = self.request.GET.get('search', '').strip()

        return super().get_queryset().filter(
            Q(title__icontains=self._search_value) |
            Q(excerpt__icontains=self._search_value) |
            Q(content__icontains=self._search_value)
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context.update(
            {
                'page_title': f'Pesquisa: {self._search_value} - ',
                'search_value': self._search_value
            }
        )

        return context


class CreatedByListView(BaseListView):
    """View para pesquisas por autor"""

    allow_empty = False

    def get_queryset(self):
        author_id = self.kwargs.get('author_id')
        return super().get_queryset().filter(created_by_id=author_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        post = self.object_list.first()
        user = post.created_by

        if user:
            author = user.username

            if user.first_name and user.last_name:
                author = f'{user.first_name} {user.last_name}'

            context.update(
                {'page_title': f'Posts de {author} - '}
            )

        return context


class CategoryListView(BaseListView):
    """View para pesquisas por categoria"""

    allow_empty = False

    def get_queryset(self):
        slug = self.kwargs.get('slug')
        return super().get_queryset().filter(category__slug=slug)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        category = self.object_list.first().category.name
        context.update(
            {'page_title': f'Categoria: {category} - '}
        )

        return context


class TagListView(BaseListView):
    """View para pesquisas por tag"""

    allow_empty = False

    def get_queryset(self):
        slug = self.kwargs.get('slug')
        return super().get_queryset().filter(tags__slug=slug)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        tag = self.object_list[0].tags.first().name
        context.update(
            {'page_title': f'Tag: {tag} - '}
        )

        return context


def page(request, slug: str):
    """View para page.html"""

    page = get_object_or_404(Page, slug=slug, is_published=True)

    return render(
        request,
        'blog/pages/page.html',
        {
            'page': page,
        }
    )


def post(request, slug: str):
    """View para post.html"""

    post = get_object_or_404(Post, slug=slug, is_published=True)

    return render(
        request,
        'blog/pages/post.html',
        {
            'post': post
        }
    )

# Function based views
#
# def index(request):
#     posts = Post.objects.get_published()
#
#     paginator = Paginator(posts, PER_PAGE)
#     page_number = request.GET.get("page")
#     page_obj = paginator.get_page(page_number)
#
#     return render(
#         request,
#         'blog/pages/index.html',
#         {
#             'page_obj': page_obj,
#             'page_title': 'Home - '
#         }
#     )
#
#
# def created_by(request, author_id: int):
#     posts = Post.objects.get_published().filter(created_by_id=author_id)
#
#     if posts:
#         user = posts[0].created_by
#
#         if user.first_name and user.last_name:
#             page_title = f'{user.first_name} {user.last_name}'
#         else:
#             page_title = user.username
#     else:
#         page_title = 'Nada encontrado'
#
#     paginator = Paginator(posts, PER_PAGE)
#     page_number = request.GET.get("page")
#     page_obj = paginator.get_page(page_number)
#
#     return render(
#         request,
#         'blog/pages/index.html',
#         {
#             'page_obj': page_obj,
#             'page_title': f'{page_title} - ',
#         }
#     )
#
#
# def category(request, slug: str):
#     posts = Post.objects.get_published().filter(category__slug=slug)
#
#     paginator = Paginator(posts, PER_PAGE)
#     page_number = request.GET.get("page")
#     page_obj = paginator.get_page(page_number)
#
#     return render(
#         request,
#         'blog/pages/index.html',
#         {
#             'page_obj': page_obj,
#         }
#     )
#
#
# def tag(request, slug: str):
#     posts = Post.objects.get_published().filter(tags__slug=slug)
#
#     paginator = Paginator(posts, PER_PAGE)
#     page_number = request.GET.get("page")
#     page_obj = paginator.get_page(page_number)
#
#     return render(
#         request,
#         'blog/pages/index.html',
#         {
#             'page_obj': page_obj,
#         }
#     )
#
#
# def search(request):
#     search_value = request.GET.get('search', '').strip()
#     posts = Post.objects.get_published().filter(
#         Q(title__icontains=search_value) |
#         Q(excerpt__icontains=search_value) |
#         Q(content__icontains=search_value)
#     )
#
#     paginator = Paginator(posts, PER_PAGE)
#     page_number = request.GET.get("page")
#     page_obj = paginator.get_page(page_number)
#
#     return render(
#         request,
#         'blog/pages/index.html',
#         {
#             'page_obj': page_obj,
#             'search_value': search_value,
#         }
#     )
#
