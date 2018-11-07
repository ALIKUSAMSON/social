from django.contrib import admin
from .models import Profile

# Register your models here.
admin.site.password_change_template = 'registration/password_change_form.html'
class ProfileAdmin(admin.ModelAdmin):
	list_display = ['user', 'date_of_birth','sex', 'photo']

admin.site.register(Profile, ProfileAdmin)