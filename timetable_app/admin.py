from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.contrib.auth.models import Group

# Register custom groups
admin.site.unregister(Group)

class GroupAdmin(admin.ModelAdmin):
    list_display = ('name',)

admin.site.register(Group, GroupAdmin)
