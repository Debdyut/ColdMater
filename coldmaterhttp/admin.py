from django.contrib import admin

from .models import User

class UserAdmin(admin.ModelAdmin):
	list_display = ['userid', 'fname', 'lname', 'org', 'orgtype', 'username', 'machineid']

admin.site.register(User, UserAdmin)
