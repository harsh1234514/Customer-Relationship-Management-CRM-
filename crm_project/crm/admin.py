from django.contrib import admin
from .models import Company, Contact, Lead, Deal, Activity

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ['name', 'industry', 'city', 'country', 'created_at']
    list_filter = ['industry', 'country', 'created_at']
    search_fields = ['name', 'industry', 'city']
    ordering = ['name']

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'email', 'company', 'contact_type', 'assigned_to', 'created_at']
    list_filter = ['contact_type', 'company', 'assigned_to', 'created_at']
    search_fields = ['first_name', 'last_name', 'email', 'company__name']
    ordering = ['last_name', 'first_name']
    raw_id_fields = ['company']

@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'email', 'company_name', 'status', 'source', 'assigned_to', 'created_at']
    list_filter = ['status', 'source', 'assigned_to', 'created_at']
    search_fields = ['first_name', 'last_name', 'email', 'company_name']
    ordering = ['-created_at']

    def full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"
    full_name.short_description = 'Name'

@admin.register(Deal)
class DealAdmin(admin.ModelAdmin):
    list_display = ['title', 'company', 'contact', 'amount', 'stage', 'probability', 'expected_close_date', 'assigned_to']
    list_filter = ['stage', 'priority', 'assigned_to', 'expected_close_date']
    search_fields = ['title', 'company__name', 'contact__first_name', 'contact__last_name']
    ordering = ['-created_at']
    raw_id_fields = ['contact', 'company']

@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ['title', 'activity_type', 'status', 'contact', 'deal', 'assigned_to', 'due_date']
    list_filter = ['activity_type', 'status', 'assigned_to', 'due_date']
    search_fields = ['title', 'contact__first_name', 'contact__last_name', 'deal__title']
    ordering = ['due_date']
    raw_id_fields = ['contact', 'deal']
