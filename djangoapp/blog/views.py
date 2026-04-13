from typing import Any

from django.core.paginator import Paginator
from django.http import Http404
from django.shortcuts import render
from blog.models import Post, Page
from django.db.models import Q, QuerySet
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView

    # Function Based Views -> Are functions
    # Class Based Views -> Are classes (POO)
    
    # Obter dados do model
    # Esses dados são uma lista de objetos
    # Paginação
    # Renderizar o template passando os dados
    # Manipular o template para exibir os dados
PER_PAGE = 9

class PostListView(ListView):
    model = Post
    template_name = 'blog/pages/index.html'
    context_object_name = 'posts'
    ordering = 'title'
    paginate_by = PER_PAGE
    queryset = Post.objects.get_published()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Home -'
        return context

class CreatedByListView(PostListView):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._temp_context: dict[str, any] = {}

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        author_pk = self.kwargs.get('author_pk')
        user = User.objects.filter(pk=author_pk).first()
        if not user:
            raise Http404()
        
        user_full_name = user.username
        if user.first_name and user.last_name:
            user_full_name = f'{user.first_name} {user.last_name}'
        ctx['page_title'] = f'Posts by {user_full_name} -'

        ctx['user'] = user
        return ctx
    
    def get_queryset(self) -> QuerySet[Any]:
        qs = super().get_queryset()
        qs = qs.filter(created_by__pk=self.kwargs.get('author_pk'))
        return qs
    

    def get(self, request, *args, **kwargs):
        author_pk = self.kwargs.get('author_pk')
        user = User.objects.filter(pk=author_pk).first()

        if user is None:
            raise Http404()

        self._temp_context.update({
            'author_pk': author_pk,
            'user': user,
        })

        return super().get(request, *args, **kwargs)

class CategoryListView(PostListView):
    allow_empty = False

    def get_queryset(self) -> QuerySet[Any]:
        qs = super().get_queryset()
        qs = qs.filter(category__slug=self.kwargs.get('slug'))
        return qs
    
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        category_name = self.get_queryset().first().category.name
        ctx['page_title'] = f'{category_name} - Category -'
        return ctx

class TagListView(PostListView):
    allow_empty = False

    def get_queryset(self) -> QuerySet[Any]:
        qs = super().get_queryset()
        qs = qs.filter(tags__slug=self.kwargs.get('slug'))
        return qs
    
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        tag_name = self.get_queryset().first().tags.first().name
        ctx['page_title'] = f'{tag_name} - Tag -'
        return ctx

class SearchListView(PostListView):
    def get_queryset(self) -> QuerySet[Any]:
        search_value = self.request.GET.get('search', '').strip()
        qs = super().get_queryset()
        qs = qs.filter(
            Q(title__icontains=search_value) |
            Q(content__icontains=search_value) |
            Q(excerpt__icontains=search_value)
        )
        return qs
    
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        search_value = self.request.GET.get('search', '').strip()
        ctx['search_value'] = search_value
        ctx['page_title'] = f'{search_value[:30]} - Search - '
        return ctx

class PageDetailView(DetailView):
    model = Page
    template_name = 'blog/pages/page.html'
    slug_field = 'slug'
    context_object_name = 'page'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        ctx = super().get_context_data(**kwargs)
        page_obj: Page = self.get_object()
        ctx['page_title'] = f'{page_obj.title} - Page '
        return ctx
    
    def get_queryset(self) -> QuerySet[Any]:
        return super().get_queryset().filter(is_published=True)

class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/pages/post.html'
    slug_field = 'slug'
    context_object_name = 'post'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        ctx = super().get_context_data(**kwargs)
        post_obj: Post = self.get_object()
        ctx['page_title'] = f'{post_obj.title} - Post - '
        return ctx
    
    def get_queryset(self) -> QuerySet[Any]:
        return super().get_queryset().filter(is_published=True)

