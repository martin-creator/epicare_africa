from django.contrib import admin
from .models import Product, Category, BlogPost, Order, ContactSubmission, NewsletterSubscription, JobOpening, JobApplication

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock', 'category')
    search_fields = ('name', 'description')
    list_filter = ('category',)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'is_featured')
    search_fields = ('title', 'content')
    list_filter = ('is_featured', 'tags')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'quantity', 'email', 'status', 'created_at')
    search_fields = ('email', 'product__name')
    list_filter = ('status',)

@admin.register(ContactSubmission)
class ContactSubmissionAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'submitted_at')
    search_fields = ('name', 'email')

@admin.register(NewsletterSubscription)
class NewsletterSubscriptionAdmin(admin.ModelAdmin):
    list_display = ('email', 'subscribed_at')
    search_fields = ('email',)
    actions = ['export_to_csv']

    def export_to_csv(self, request, queryset):
        from .views import export_newsletter_csv
        return export_newsletter_csv(request)
    export_to_csv.short_description = "Export selected subscriptions to CSV"


@admin.register(JobOpening)
class JobOpeningAdmin(admin.ModelAdmin):
    list_display = ('title', 'department', 'location', 'is_active', 'created_at')
    search_fields = ('title', 'department', 'location')
    list_filter = ('is_active',)


@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'position', 'resume', 'cover_letter', 'submitted_at')
    search_fields = ('name', 'email', 'position')
    list_filter = ('position',)
    actions = ['export_to_csv']

    def export_to_csv(self, request, queryset):
        from .views import export_job_applications_csv
        return export_job_applications_csv(request)
    export_to_csv.short_description = "Export selected applications to CSV"    