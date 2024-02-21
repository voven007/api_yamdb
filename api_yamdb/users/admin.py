from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin
from users.models import MyUser


@admin.register(MyUser)
class MyUserAdmin(admin.ModelAdmin):
    list_display = (
        'username', 'email', 'first_name', 'last_name', 'bio', 'role')
    search_fields = (
        'username', 'email', 'first_name', 'last_name', 'role')
