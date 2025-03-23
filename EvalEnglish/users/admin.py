from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, TeacherApplication
from django.utils import timezone
from django.core.mail import send_mail
from django.contrib.contenttypes.admin import GenericTabularInline
from common.models import Document

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('id', 'email', 'first_name', 'last_name', 'role', 'is_teacher', 'is_active', 'date_joined')
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

class DocumentInline(GenericTabularInline):
    model = Document
    extra = 1
    readonly_fields = ('uploaded_at',)
    # Опционально: ограничение типов файлов
    # formfield_overrides = {
    #     models.FileField: {'widget': admin.widgets.AdminFileWidget},
    # }

@admin.register(TeacherApplication)
class TeacherApplicationAdmin(admin.ModelAdmin):
    list_display = ('user', 'full_name', 'phone', 'status', 'submitted_at', 'reviewed_at')
    list_filter = ('status',)
    search_fields = ('user__email', 'full_name', 'phone')
    readonly_fields = ('submitted_at', 'reviewed_at')
    inlines = [DocumentInline] 

    actions = ['approve_applications', 'reject_applications']

    def approve_applications(self, request, queryset):
        for application in queryset:
            if application.status != 'approved':
                application.status = 'approved'
                application.reviewed_at = timezone.now()
                application.save()
                
                user = application.user
                user.is_teacher = True
                user.save()
                
                send_mail(
                    "Ваша заявка одобрена",
                    "Поздравляем! Ваша заявка на преподавателя была одобрена.",
                    "noreply@evalenglish.com",
                    [user.email],
                    fail_silently=False,
                )
        self.message_user(request, "Выбранные заявки успешно одобрены.")

    approve_applications.short_description = "Одобрить выбранные заявки"

    def reject_applications(self, request, queryset):
        for application in queryset:
            if application.status != 'rejected':
                application.status = 'rejected'
                application.reviewed_at = timezone.now()
                application.save()
                
                send_mail(
                    "Ваша заявка отклонена",
                    "К сожалению, ваша заявка на преподавателя была отклонена.",
                    "noreply@evalenglish.com",
                    [application.user.email],
                    fail_silently=False,
                )
        self.message_user(request, "Выбранные заявки успешно отклонены.")

    reject_applications.short_description = "Отклонить выбранные заявки"

