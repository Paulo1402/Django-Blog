from django.urls import path
from blog.views import index, post, page, created_by, category

app_name = 'blog'

urlpatterns = [
    path('', index, name='index'),
    path('post/<slug:slug>/', post, name='post'),
    path('page/<slug:slug>/', page, name='page'),
    path('category/<slug:slug>/', category, name='category'),
    path('created_by/<int:author_id>/', created_by, name='created_by'),
]
