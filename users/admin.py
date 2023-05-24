from django.contrib import admin

from users.models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'username', 'is_admin', 'date',)
    list_filter = ('is_admin',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('username',)}),
        ('Permissions', {'fields': ('is_admin',)}),
        ('Createdate', {'fields': ('date',)}),

    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2',),
        }),
    )
    search_fields = ('email',)
    filter_horizontal = ()
    ordering = ('email',)


admin.site.register(User, UserAdmin)
