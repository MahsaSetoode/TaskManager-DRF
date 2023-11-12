from django.contrib import admin
from . import models

# Register models:
# admin.site.register(models.Task)
# or (to customize the fields)
@admin.register(models.Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['title', 'status', 'description', 'owner', 'created_at', 'updated_at' ]
    list_editable = ['status']
    search_fields = ['title', 'description']