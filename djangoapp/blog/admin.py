from django.contrib import admin
from blog.models import Category, Tag, Page, Post
from django_summernote.admin import SummernoteModelAdmin
from django.urls import reverse
from django.utils.safestring import mark_safe


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = 'id', 'name', 'slug',
    list_display_links = 'name',
    search_fields = 'id', 'name', 'slug',
    list_per_page = 10
    ordering = "-id",
    prepopulated_fields = {'slug': ('name',),}

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = 'id', 'name', 'slug',
    list_display_links = 'name',
    search_fields = 'id', 'name', 'slug',
    list_per_page = 10
    ordering = "-id",
    prepopulated_fields = {'slug': ('name',),}

@admin.register(Page)
class PageAdmin(SummernoteModelAdmin):
    summernote_fields = 'content',
    list_display = 'id', 'title', 'slug', 'is_published',
    list_display_links = 'title',
    search_fields = 'id', 'title', 'slug',
    list_per_page = 10
    ordering = "-id",
    prepopulated_fields = {'slug': ('title',),}

@admin.register(Post)
class PostAdmin(SummernoteModelAdmin):
    summernote_fields = 'content',
    list_display = 'id', 'title', 'slug', 'is_published',
    list_display_links = 'title',
    search_fields = 'id', 'title', 'slug', 'excerpt', 'content',
    list_per_page = 50
    list_filter = 'is_published', 'category',
    list_editable = 'is_published',
    ordering = "-id",
    readonly_fields = 'created_at', 'updated_at', 'created_by', 'updated_by', \
        'link',
    prepopulated_fields = {'slug': ('title',),}
    autocomplete_fields = 'tags', 'category',

    def link(self, obj):
        if not obj.pk:
            return "Save and continue editing to view the link"
        
        url_do_post = obj.get_absolute_url()
        return mark_safe(f'<a href="{url_do_post}" target="_blank">{obj.title}</a>')

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.created_by = request.user
        else:
            obj.updated_by = request.user
        super().save_model(request, obj, form, change)