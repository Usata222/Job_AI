from django.contrib import admin

from .forms import ProfileAdminForm
from .models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    form = ProfileAdminForm
    list_display = ('user', 'target_role', 'country', 'updated_at')
    search_fields = ('user__email', 'target_role')