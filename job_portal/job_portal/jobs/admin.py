from django.contrib import admin
from django.contrib import messages
from django.db import IntegrityError
from .models import Job, Company, JobRegisteredUsers
class JobAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        try:
            super().save_model(request, obj, form, change)
        except IntegrityError as e:
            messages.error(request, "Failed to add the job due to a foreign key constraint error.")
admin.site.unregister(Job)
admin.site.register(Job, JobAdmin)  # Ensure this is only called once
admin.site.register(Company)
@admin.register(JobRegisteredUsers)
class JobRegisteredUsersAdmin(admin.ModelAdmin):
    list_display = ('user', 'job', 'registered_at')
    search_fields = ('user__username', 'job__role', 'job__company_name')
    list_filter = ('registered_at',)