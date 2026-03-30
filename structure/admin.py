from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .models import Application, Specialist, Portfolio, WorkMethods, PortfolioMethods

User = get_user_model()


@admin.register(User)
class UserAdmin(UserAdmin):
    list_display = ('first_name', 'middle_name', 'last_name', 'email',
                    'phone_number', 'is_active', 'role', 'password')
    search_fields = ('email', 'phone_number')

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('cite', {
            'fields': (
                'first_name',
                'middle_name',
                'last_name',
                'email',
                'phone_number',
                'role',
            )
        }),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('email', 'resume_file')
    search_fields = ('email',)


@admin.register(Specialist)
class SpecialistAdmin(admin.ModelAdmin):
    list_display = ('user', 'portfolio', 'link', 'work_email')
    search_fields = ('work_email',)


@admin.register(WorkMethods)
class WorkMethodsAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ('title',)


class PortfolioMethodsInline(admin.TabularInline):
    model = PortfolioMethods
    extra = 1


@admin.register(Portfolio)
class PortfolioAdmin(admin.ModelAdmin):
    inlines = [PortfolioMethodsInline]
    list_display = ('education', 'practice', 'description', 'image')
    search_fields = ('user__email',)
