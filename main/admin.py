from django.contrib import admin

from .models import *


@admin.register(ClientProfile)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('passport', 'phone',)
    list_display_links = ('passport', 'phone',)
    search_fields = ('passport', 'phone',)


@admin.register(TeacherProfile)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('education_certificate', 'profession', 'home',)
    list_display_links = ('education_certificate', 'profession', 'home',)
    search_fields = ('education_certificate', 'profession', 'home',)


@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    pass


@admin.register(Style)
class StyleAdmin(admin.ModelAdmin):
    pass


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    pass
