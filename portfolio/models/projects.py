from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify

class Technology(models.Model):
    name = models.CharField(max_length=100, verbose_name=_("Name"))
    icon = models.CharField(max_length=50, verbose_name=_("Icon"), null=True, blank=True)
    display_order = models.PositiveIntegerField(default=0, verbose_name=_("Display Order"))

    class Meta:
        verbose_name = _("Technology")
        verbose_name_plural = _("Technologies")
        ordering = ["display_order"]

    def __str__(self):
        return self.name


class Project(models.Model):
    STATUS_CHOICES = [
        ("completed", "Completed"),
        ("in_progress", "In Progress"),
        ("on_hold", "On Hold"),
    ]

    title = models.CharField(max_length=200, verbose_name=_("Title"))
    slug = models.SlugField(max_length=200, unique=True, verbose_name=_("Slug"))
    short_description = models.TextField(verbose_name=_("Short Description"))
    description = models.TextField(verbose_name=_("Description"))
    challenge = models.TextField(verbose_name=_("Challenge"), null=True, blank=True)
    solution = models.TextField(verbose_name=_("Solution"), null=True, blank=True)
    results = models.TextField(verbose_name=_("Results"), null=True, blank=True)
    cover_image = models.ImageField(
        upload_to="projects/",
        verbose_name=_("Cover Image"),
        null=True,
        blank=True,
    )
    client_name = models.CharField(max_length=200, verbose_name=_("Client Name"), null=True, blank=True)
    project_date = models.DateField(verbose_name=_("Project Date"))
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="completed",
        verbose_name=_("Status"),
    )
    live_url = models.URLField(verbose_name=_("Live URL"), null=True, blank=True)
    github_url = models.URLField(verbose_name=_("GitHub URL"), null=True, blank=True)
    technologies = models.ManyToManyField(
        Technology,
        related_name="projects",
        verbose_name=_("Technologies"),
    )
    is_featured = models.BooleanField(default=False, verbose_name=_("Is Featured"))
    is_published = models.BooleanField(default=True, verbose_name=_("Is Published"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated At"))

    class Meta:
        verbose_name = _("Project")
        verbose_name_plural = _("Projects")
        ordering = ["-project_date"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class ProjectImage(models.Model):
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="images",
        verbose_name=_("Project"),
    )
    image = models.ImageField(
        upload_to="projects/images/",
        verbose_name=_("Image"),
    )
    caption = models.CharField(max_length=200, verbose_name=_("Caption"), null=True, blank=True)
    display_order = models.PositiveIntegerField(default=0, verbose_name=_("Display Order"))

    class Meta:
        verbose_name = _("Project Image")
        verbose_name_plural = _("Project Images")
        ordering = ["display_order"]

    def __str__(self):
        return f"{self.project.title} - Image {self.id}"