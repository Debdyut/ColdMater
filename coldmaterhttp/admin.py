from django.contrib import admin

from .models import User, Machine

class UserAdmin(admin.ModelAdmin):
	list_display = ['userid', 'fname', 'lname', 'org', 'orgtype', 'username', 'machineid']

class MachineAdmin(admin.ModelAdmin):
	list_display = ['machineid', 'machine_status', 'ambient_temp', 'water_temp', 'set_temp', 'temp_set_by']

admin.site.register(User, UserAdmin)
admin.site.register(Machine, MachineAdmin)
