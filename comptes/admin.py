from django.contrib import admin
from .models import Members, GroupProfile
from django.contrib.auth.admin import UserAdmin
from .forms import UserCreationForm, UserChangeForm

# Register your models here.

class UserAdmin(UserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    list_display = ('email', 'phone_number', 'first_name', 'is_active', 'date_joined')
    list_filter = ('is_active', 'is_staff', 'is_superuser')
    fieldsets = (
        (None, {'fields': ('password', 'email', 'first_name', 'last_name', 'phone_number', 'image', 'latitude', 'longitude')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser',  'groups', 'user_permissions')}),
        ('Important date', {'fields': ('last_login', )})
    )
    add_fieldsets = (
        (None, {'fields': ('first_name', 'phone_number', 'email', 'password_1', 'password_2')}),
    )
    search_fields = ('email', 'first_name', 'phone_number')
    ordering = ('email',)
    filter_horizontal = ('groups', 'user_permissions')


admin.site.register(Members, UserAdmin)
admin.site.register(GroupProfile)