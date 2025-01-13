from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, TeacherApplication

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    # Поля, отображаемые в списке пользователей
    list_display = ('email', 'first_name', 'last_name', 'role', 'is_teacher', 'is_active', 'date_joined')
    list_filter = ('role', 'is_teacher', 'is_active', 'date_joined')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('-date_joined',)

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'avatar')}),
        ('Permissions', {'fields': ('role', 'is_teacher', 'is_active', 'is_staff', 'is_superuser')}),
        ('Important Dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'first_name', 'last_name', 'role', 'avatar'),
        }),
    )

class DocumentInline(admin.TabularInline):
    model = TeacherApplication.document.through
    extra = 1

@admin.register(TeacherApplication)
class TeacherApplicationAdmin(admin.ModelAdmin):
    inlines = [DocumentInline]
    list_display = ('user', 'status', 'submitted_at', 'reviewed_at')
    list_filter = ('status', 'submitted_at')
    search_fields = ('user__email', 'user__first_name', 'user__last_name')
    readonly_fields = ('submitted_at',)
