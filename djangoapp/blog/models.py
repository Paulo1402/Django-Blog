from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django_summernote.models import AbstractAttachment

from utils import slugify_new, resize_image


class PostAttachment(AbstractAttachment):
    def save(self, *args, **kwargs):
        if not self.name:
            self.name = self.file.name

        current_file_name = str(self.file.name)
        super().save(*args, **kwargs)

        if self.file:
            file_changed = current_file_name != self.file.name

            if file_changed:
                resize_image(self.file, new_width=900)


class Tag(models.Model):
    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'

    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, default=None, null=True, blank=True, max_length=255)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify_new(self.name, k=5)

        return super().save(*args, **kwargs)


class Category(models.Model):
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, default=None, null=True, blank=True, max_length=255)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify_new(self.name, k=5)

        return super().save(*args, **kwargs)


class Page(models.Model):
    title = models.CharField(max_length=65)
    slug = models.SlugField(unique=True, default='', null=False, blank=True, max_length=255)
    is_published = models.BooleanField(
        default=False,
        help_text='Este campo precisará estar marcado para a página ser exibida publicamente.'
    )
    content = models.TextField()

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify_new(self.title, k=5)

        return super().save(*args, **kwargs)


class PostManager(models.Manager):
    def get_published(self):
        return self.filter(is_published=True).order_by('-pk')


class Post(models.Model):
    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'

    objects = PostManager()

    title = models.CharField(max_length=65)
    slug = models.SlugField(unique=True, default='', null=False, blank=True, max_length=255)
    excerpt = models.CharField(max_length=150)
    is_published = models.BooleanField(
        default=False,
        help_text='Esse campo precisará estar marcado para o post ser exibido publicamente.'
    )
    content = models.TextField()
    cover = models.ImageField(upload_to='posts/%Y/%m/', blank=True, default='')
    cover_in_post_content = models.BooleanField(
        default=True,
        help_text='Se marcado, exibirá a capa dentro do post.'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    # Podemos acessar esse model através do model User usando: user.post_created_by.all
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='post_created_by'
    )
    updated_at = models.DateTimeField(auto_now=True)
    # Podemos acessar esse model através do model User usando: user.post_updated_by.all
    updated_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='post_updated_by'
    )
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True, default=None
    )
    tags = models.ManyToManyField(Tag, blank=True, default='')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        if not self.is_published:
            return reverse('blog:index')

        return reverse('blog:post', args=(self.slug,))

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify_new(self.title, k=5)

        current_cover_name = str(self.cover.name)
        super().save(*args, **kwargs)

        if self.cover:
            cover_changed = current_cover_name != self.cover.name

            if cover_changed:
                resize_image(self.cover, new_width=900)
