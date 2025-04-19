from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, TemplateView
from .models import Post, Category


# Наследуем класс от встроенного ListView:
class PostListView(ListView):
    # Указываем модель, с которой работает CBV...
    model = Post
    # По умолчанию этот класс
    # выполняет запрос queryset = Post.objects.all(),
    # но мы его переопределим:
    queryset = Post.objects.filter(
        pub_date__date__lt=timezone.now(),
        is_published=True,
        category__is_published=True
    ).select_related('author', 'location', 'category')
    # ...сортировку, которая будет применена при выводе списка объектов:
    ordering = '-pub_date'
    # ...и даже настройки пагинации:
    paginate_by = 5
    template_name = 'blog/index.html'


class PostDetailPage(TemplateView):
    template_name = 'blog/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post'] = get_object_or_404(
            Post,
            pk=self.kwargs['post_id'],
            is_published=True,
            category__is_published=True,
            pub_date__date__lt=timezone.now()
        )
        return context


class CategoryPostsListView(ListView):
    model = Post
    ordering = '-pub_date'
    template_name = 'blog/category.html'

    def get_queryset(self):
        # Получаем slug категории из URL
        category_slug = self.kwargs.get('category')

        # Получаем объект категории или вызываем 404,
        # если не найдено или не опубликовано
        self.category = get_object_or_404(
            Category, slug=category_slug, is_published=True
        )

        # Фильтруем посты по категории и другим условиям
        queryset = self.category.posts.filter(
            category=self.category,
            pub_date__date__lt=timezone.now(),
            is_published=True,
        ).select_related('author', 'location', 'category')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавляем объект категории в контекст для использования в шаблоне
        context['category'] = self.category
        return context
