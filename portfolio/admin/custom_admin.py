from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from portfolio.models import (
    Profile,
    SocialLink,
    Service,
    ServiceFeature,
    Project,
    ProjectImage,
    Technology,
    Experience,
    Testimonial,
    ContactMessage,
    SEO,
    SiteSettings,
    Tool,
)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("full_name", "professional_title", "email", "availability_status")
    list_filter = ("availability_status",)
    search_fields = ("full_name", "professional_name", "email")
    fieldsets = (
        (_("Identity"), {
            "fields": ("full_name", "professional_name", "professional_title", "profile_image", "logo")
        }),
        (_("Biography"), {
            "fields": ("short_bio", "biography")
        }),
        (_("Location"), {
            "fields": ("location", "country", "city")
        }),
        (_("Contact"), {
            "fields": ("email", "phone", "whatsapp")
        }),
        (_("Availability"), {
            "fields": ("availability_status", "availability_message")
        }),
        (_("Resume"), {
            "fields": ("resume_file",)
        }),
    )


@admin.register(SocialLink)
class SocialLinkAdmin(admin.ModelAdmin):
    list_display = ("name", "platform", "url", "is_active", "display_order")
    list_filter = ("platform", "is_active")
    search_fields = ("name", "url")
    ordering = ("display_order",)


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("title", "is_featured", "is_active", "display_order")
    list_filter = ("is_featured", "is_active")
    search_fields = ("title", "short_description")
    prepopulated_fields = {"slug": ("title",)}
    ordering = ("display_order",)
    fieldsets = (
        (_("Core"), {
            "fields": ("title", "slug", "short_description", "description", "icon", "image")
        }),
        (_("Detail Page Content"), {
            "fields": (
                "hero_description", "problem", "audience", "features",
                "concrete_example", "how_it_works", "before_after",
                "benefits", "included", "technical_details",
            ),
            "classes": ("collapse",),
        }),
        (_("Visibility"), {
            "fields": ("is_featured", "is_active", "display_order")
        }),
    )


@admin.register(ServiceFeature)
class ServiceFeatureAdmin(admin.ModelAdmin):
    list_display = ("service", "feature", "display_order")
    list_filter = ("service",)
    ordering = ("display_order",)


class ProjectImageInline(admin.TabularInline):
    model = ProjectImage
    extra = 1


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("title", "client_name", "project_date", "status", "is_featured", "is_published")
    list_filter = ("status", "is_featured", "is_published", "technologies")
    search_fields = ("title", "client_name", "short_description")
    prepopulated_fields = {"slug": ("title",)}
    inlines = [ProjectImageInline]
    filter_horizontal = ("technologies",)
    fieldsets = (
        (_("Core"), {
            "fields": ("title", "slug", "short_description")
        }),
        (_("Case Study"), {
            "fields": ("context", "problem", "approach", "solution", "features", "result", "role"),
            "classes": ("collapse",),
        }),
        (_("Legacy Fields"), {
            "fields": ("description", "challenge", "results"),
            "classes": ("collapse",),
        }),
        (_("Media"), {
            "fields": ("cover_image",)
        }),
        (_("Metadata"), {
            "fields": ("client_name", "project_date", "status", "live_url", "github_url", "technologies")
        }),
        (_("Visibility"), {
            "fields": ("is_featured", "is_published")
        }),
    )


@admin.register(ProjectImage)
class ProjectImageAdmin(admin.ModelAdmin):
    list_display = ("project", "caption", "display_order")
    list_filter = ("project",)


@admin.register(Technology)
class TechnologyAdmin(admin.ModelAdmin):
    list_display = ("name", "display_order")
    search_fields = ("name",)


@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ("title", "organization", "start_date", "end_date", "is_current", "display_order")
    list_filter = ("type", "is_current", "is_published")
    search_fields = ("title", "organization")
    ordering = ("-start_date",)
    filter_horizontal = ("related_projects", "technologies")
    fieldsets = (
        (_("Core"), {
            "fields": ("title", "organization", "location", "start_date", "end_date", "is_current", "type")
        }),
        (_("Content"), {
            "fields": ("role", "description", "responsibilities", "tasks", "achievements", "results")
        }),
        (_("Relations"), {
            "fields": ("related_projects", "technologies")
        }),
        (_("Display"), {
            "fields": ("display_order", "is_published")
        }),
    )


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ("name", "position", "company", "is_featured", "is_active", "display_order")
    list_filter = ("is_featured", "is_active")
    search_fields = ("name", "position", "company")


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "email", "subject", "is_read", "created_at")
    list_filter = ("is_read", "service", "budget")
    search_fields = ("first_name", "last_name", "email", "subject")
    readonly_fields = ("created_at",)


@admin.register(SEO)
class SEOAdmin(admin.ModelAdmin):
    list_display = ("page", "seo_title")
    search_fields = ("page", "seo_title")


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ("site_name", "slogan", "is_active", "maintenance_mode")


@admin.register(Tool)
class ToolAdmin(admin.ModelAdmin):
    list_display = ("name", "icon", "category", "display_order", "is_active")
    list_filter = ("category", "is_active")
    search_fields = ("name",)
    ordering = ("display_order", "name")
