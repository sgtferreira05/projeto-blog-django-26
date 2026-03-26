from django.db import models
from django.urls import reverse
from utils.rands import slugify_new
from django.contrib.auth.models import User
from utils.images import resize_image
from django_summernote.models import AbstractAttachment, Attachment

class PostAttachment(AbstractAttachment):
    def save(self, *args, **kwargs):
        if not self.name:
            self.name = self.file.name
        
        current_file_name = str(self.file.name)
        super_save = super().save(*args, **kwargs)
        file_changed = False

        if self.file:
            file_changed = (current_file_name != str(self.file.name))
        
        if file_changed:
            resize_image(self.file, 900, True, 70)
        return super_save


class Tag(models.Model):
    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'
    name = models.CharField(max_length=50)
    slug = models.SlugField(
        max_length=50, unique=True, default=None, null=True, blank=True
        )
    url_externa = models.URLField(
        max_length=255, blank=True, default='',
        help_text='URL externa para a tag. Se preenchida, a tag redirecionará para essa URL em vez de exibir os posts associados.'
    )
    nova_aba = models.BooleanField(
        default=False
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify_new(self.name, 2)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Category(models.Model):
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
    name = models.CharField(max_length=50)
    slug = models.SlugField(
        max_length=50, unique=True, default=None, null=True, blank=True
        )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify_new(self.name, 2)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Page(models.Model):
    class Meta:
        verbose_name = 'Page'
        verbose_name_plural = 'Pages'
    title = models.CharField(max_length=50)
    slug = models.SlugField(
        max_length=50, unique=True, default=None, null=True, blank=True
        )
    is_published = models.BooleanField(
        default=False,
        help_text='Indicates whether the page is published or not.'        
        )
    content = models.TextField()
    
    def get_absolute_url(self):
        if not self.is_published:
            return reverse("blog:index")
        return reverse("blog:page", args={self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify_new(self.title, 2)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class PostManager(models.Manager):
    def get_published(self):
        return self.filter(is_published=True).order_by('title')

class Post(models.Model):
    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'

    objects = PostManager()

    title = models.CharField(max_length=50)
    slug = models.SlugField(
        max_length=50, unique=True, default=None, null=True, blank=True
        )
    excerpt = models.CharField(max_length=255, blank=True)
    is_published = models.BooleanField(
        default=False,
        help_text='Indicates whether the post is published or not.'        
        )
    content = models.TextField()
    cover = models.ImageField(upload_to='posts/%Y/%m/', blank=True, default='')
    cover_in_post_content = models.BooleanField(
        default=False,
        help_text='Indicates whether the cover image should be included in the post content.'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    # user.post_created_by.all() -> posts criados por um usuário
    created_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name='post_created_by'
    )
    updated_at = models.DateTimeField(auto_now=True)
    # user.post_updated_by.all() -> posts atualizados por um usuário
    updated_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name='post_updated_by'
    )

    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True
        )
    tags = models.ManyToManyField(Tag, blank=True)

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        if not self.is_published:
            return reverse("blog:index")
        return reverse("blog:post", kwargs={"slug": self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify_new(self.title, 2)        

        current_cover_name = str(self.cover.name)
        super_save = super().save(*args, **kwargs)
        cover_changed = False

        if self.cover:
            cover_changed = (current_cover_name != str(self.cover.name))

        if cover_changed:
            from utils.images import resize_image
            resize_image(self.cover, 900, True, 90)
        return super_save