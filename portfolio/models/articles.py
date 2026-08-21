from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from ckeditor.fields import RichTextField

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name=_("Name"))
    slug = models.SlugField(max_length=100, unique=True, verbose_name=_("Slug"))
    display_order = models.PositiveIntegerField(default=0, verbose_name=_("Display Order"))

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")
        ordering = ["display_order"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Tag(models.Model):
    name = models.CharField(max_length=100, verbose_name=_("Name"))
    slug = models.SlugField(max_length=100, unique=True, verbose_name=_("Slug"))

    class Meta:
        verbose_name = _("Tag")
        verbose_name_plural = _("Tags")

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Article(models.Model):
    STATUS_CHOICES = [
        ("draft", "Draft"),
        ("published", "Published"),
        ("archived", "Archived"),
    ]

    title = models.CharField(max_length=200, verbose_name=_("Title"))
    slug = models.SlugField(max_length=200, unique=True, verbose_name=_("Slug"))
    excerpt = models.TextField(verbose_name=_("Excerpt"))
    content = RichTextField(verbose_name=_("Content"))
    cover_image = models.ImageField(
        upload_to="articles/",
        verbose_name=_("Cover Image"),
        null=True,
        blank=True,
    )
    author = models.ForeignKey(
        "Profile",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="articles",
        verbose_name=_("Author"),
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="articles",
        verbose_name=_("Category"),
    )
    tags = models.ManyToManyField(
        Tag,
        related_name="articles",
        verbose_name=_("Tags"),
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="draft",
        verbose_name=_("Status"),
    )
    published_at = models.DateTimeField(
        verbose_name=_("Published At"),
        null=True,
        blank=True,
    )
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated At"))
    reading_time = models.PositiveIntegerField(
        default=5,
        verbose_name=_("Reading Time (minutes)"),
    )
    is_featured = models.BooleanField(default=False, verbose_name=_("Is Featured"))
    seo_title = models.CharField(
        max_length=200,
        verbose_name=_("SEO Title"),
        null=True,
        blank=True,
    )
    seo_description = models.TextField(
        verbose_name=_("SEO Description"),
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))

    class Meta:
        verbose_name = _("Article")
        verbose_name_plural = _("Articles")
        ordering = ["-published_at"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)