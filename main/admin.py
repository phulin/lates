from lates.main.models import Late
from django.contrib import admin

class LateAdmin(admin.ModelAdmin):
    list_display = ['name', 'request_date', 'is_today']

admin.site.register(Late, LateAdmin)
