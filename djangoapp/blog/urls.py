from django.urls import path
from blog.views import post, page, IndexListView, CreatedByListView, CategoryListView, TagListView, \
    SearchListView

app_name = 'blog'

urlpatterns = [
    path('', IndexListView.as_view(), name='index'),
    path('post/<slug:slug>/', post, name='post'),
    path('page/<slug:slug>/', page, name='page'),
    path('category/<slug:slug>/', CategoryListView.as_view(), name='category'),
    path('tag/<slug:slug>/', TagListView.as_view(), name='tag'),
    path('created_by/<int:author_id>/', CreatedByListView.as_view(), name='created_by'),
    path('search/', SearchListView.as_view(), name='search'),
]
