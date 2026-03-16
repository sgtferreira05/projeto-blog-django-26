from django.db import models
from utils.rands import slugify_new
from django.contrib.auth.models import User
from utils.images import resize_image

class Tag(models.Model):
    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'
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

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify_new(self.title, 2)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title



class Post(models.Model):
    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'
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