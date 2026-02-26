from django.db import models
from utils.images import resize_image

from utils.model_validator import validate_png

# Create your models here.
class MenuLink(models.Model):
    class Meta:
        verbose_name = "Menu Link"
        verbose_name_plural = "Menu Links"

    text = models.CharField(max_length=50)
    url_or_path = models.CharField(max_length=2048)
    new_tab = models.BooleanField(default=False)
    site_setup = models.ForeignKey(
        'SiteSetup',
        on_delete=models.CASCADE, null=True, blank=True, default=None,
    )

    def __str__(self):
        return self.text

class SiteSetup(models.Model):
    class Meta:
        verbose_name = "Setup"
        verbose_name_plural = "Setup"

    title = models.CharField(max_length=100)
    description = models.TextField()
    show_header = models.BooleanField(default=True)
    show_search = models.BooleanField(default=True)
    show_menu = models.BooleanField(default=True)
    show_description = models.BooleanField(default=True)
    show_paginator = models.BooleanField(default=True)
    show_footer = models.BooleanField(default=True)

    favicon = models.ImageField(
        upload_to='assets/favicon/%Y/%m',
        null=True, blank=True, default=None,
        validators=[validate_png],        
        )

    def save(self, *args, **kwargs):
            current_favicon_name = str(self.favicon.name)
            print(f"Current favicon name:" ,current_favicon_name)
            super().save(*args, **kwargs)
            favicon_changed = False

            if self.favicon:
                favicon_changed = (current_favicon_name != str(self.favicon.name))

            if favicon_changed:
                from utils.images import resize_image
                resize_image(self.favicon, new_width=32, optimize=True, quality=60)


    def __str__(self):
        return self.title
    