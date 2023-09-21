from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe

from .models import UserProfile, Cities, Payments, Address


class ProfileInline(admin.StackedInline):
    model = UserProfile
    verbose_name_plural = 'Профиль'
    fields = ('avatar', 'phone', 'preview')
    readonly_fields = ('preview', )
    fk_name = 'user'

    def preview(self, obj):
        return mark_safe(f'<img src="{obj.avatar.url}" style="max-height: 100px;">')

    preview.short_description = 'Аватар'


class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline, )
    fieldsets = (
        (None, {"fields": (
            "username",
            "password"
        )}),
        ("ЛИЧНЫЕ ДАННЫЕ", {
            "classes": ("collapse",),
            "fields": (
                ("first_name",
                "last_name"),
                "email")}),
        ("РАЗРЕШЕНИЯ", {
            "classes": ("collapse",),
            "fields": (
                "is_active",
                "is_staff",
                "is_superuser",
                "groups",
                "user_permissions")}),
        ("КЛЮЧЕВЫЕ ДАТЫ", {
            "classes": ("collapse",),
            "fields": (
                "last_login",
                "date_joined")}),
    )

    list_display = ('preview', 'username', 'email', 'first_name', 'last_name', 'get_phone')
    list_select_related = ('userprofile',)

    def preview(self, instance):
        return mark_safe(f'<img src="{instance.userprofile.avatar.url}" style="max-height: 60px;">')

    preview.short_description = 'Аватар'

    def get_phone(self, instance):
        return instance.userprofile.phone

    get_phone.short_description = 'Телефон'

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)


class CitiesAdmin(admin.ModelAdmin):
    pass


class PaymentsAdmin(admin.ModelAdmin):
    pass

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    pass


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
admin.site.register(Cities, CitiesAdmin)
admin.site.register(Payments, PaymentsAdmin)


