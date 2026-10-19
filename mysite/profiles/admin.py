from django.contrib import admin

from .models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'target_role', 'location', 'updated_at')
    search_fields = ('user__email', 'target_role', 'location')