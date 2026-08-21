from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from portfolio.models import (
    Profile,
    SocialLink,
    Statistic,
    Service,
    ServiceFeature,
    SkillCategory,
    Skill,
    Experience,
    Project,
    ProjectImage,
    Technology,
    Article,
    Category,
    Tag,
    Testimonial,
    ContactMessage,
    NewsletterSubscriber,
    SEO,
    SiteSettings,
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


@admin.register(Statistic)
class StatisticAdmin(admin.ModelAdmin):
    list_display = ("label", "value", "is_active", "display_order")
    list_filter = ("is_active",)
    search_fields = ("label",)
    ordering = ("display_order",)


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("title", "is_featured", "is_active", "display_order")
    list_filter = ("is_featured", "is_active")
    search_fields = ("title", "short_description")
    prepopulated_fields = {"slug": ("title",)}
    ordering = ("display_order",)


@admin.register(ServiceFeature)
class ServiceFeatureAdmin(admin.ModelAdmin):
    list_display = ("service", "feature", "display_order")
    list_filter = ("service",)
    ordering = ("display_order",)


@admin.register(SkillCategory)
class SkillCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "display_order")
    ordering = ("display_order",)


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "level", "years_experience", "is_featured", "display_order")
    list_filter = ("category", "level", "is_featured")
    search_fields = ("name",)
    ordering = ("display_order",)


@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ("title", "company", "start_date", "end_date", "is_current", "display_order")
    list_filter = ("type", "is_current")
    search_fields = ("title", "company")
    ordering = ("-start_date",)


class ProjectImageInline(admin.TabularInline):
    model = ProjectImage
    extra = 1


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("title", "client_name", "project_date", "status", "is_featured", "is_published")
    list_filter = ("status", "is_featured", "is_published", "technologies")
    search_fields = ("title", "client_name", "description")
    prepopulated_fields = {"slug": ("title",)}
    inlines = [ProjectImageInline]
    filter_horizontal = ("technologies",)


@admin.register(ProjectImage)
class ProjectImageAdmin(admin.ModelAdmin):
    list_display = ("project", "caption", "display_order")
    list_filter = ("project",)


@admin.register(Technology)
class TechnologyAdmin(admin.ModelAdmin):
    list_display = ("name", "display_order")
    search_fields = ("name",)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "display_order")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("name",)
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "category", "status", "published_at", "is_featured")
    list_filter = ("category", "status", "is_featured", "tags")
    search_fields = ("title", "excerpt", "content")
    prepopulated_fields = {"slug": ("title",)}
    filter_horizontal = ("tags",)


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ("name", "position", "company", "rating", "is_featured", "is_active", "display_order")
    list_filter = ("is_featured", "is_active")
    search_fields = ("name", "position", "company")


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "email", "subject", "is_read", "created_at")
    list_filter = ("is_read", "service", "budget")
    search_fields = ("first_name", "last_name", "email", "subject")
    readonly_fields = ("created_at",)


@admin.register(NewsletterSubscriber)
class NewsletterSubscriberAdmin(admin.ModelAdmin):
    list_display = ("email", "is_active", "subscribed_at")
    list_filter = ("is_active",)
    search_fields = ("email",)


@admin.register(SEO)
class SEOAdmin(admin.ModelAdmin):
    list_display = ("page", "seo_title")
    search_fields = ("page", "seo_title")


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ("site_name", "slogan", "is_active", "maintenance_mode")