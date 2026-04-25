from django.contrib import admin
from user.models import UserInfo

@admin.register(UserInfo)
class AdminUser(admin.ModelAdmin):
    list_display = ['Name', 'Class', 'Father_Name', 'Mother_Name', 'Phone_no', 'logged_in', 'created_at']

