from django.contrib import admin

# Register your models here.
from .models import *


class ClassRoomAdmin(admin.ModelAdmin):
    fieldsets = [
        # (None, {'fields': ['question_text']}),
        # ('Date information',
        # {'fields': ['pub_date'], 'classes': ['collapse']}),
    ]
    # list_display = ['name','short_name', 'numeric_name', 'class_slug', 'comment', 'updated',   ]
    # inlines = [ChoiceInline]


class ContactUsAdmin(admin.ModelAdmin):
    fieldsets = [
        # (None, {'fields': ['question_text']}),
        # ('Date information',
        # {'fields': ['pub_date'], 'classes': ['collapse']}),
    ]
    # list_display = []
    # inlines = [ChoiceInline]


class CustomizAdmin(admin.ModelAdmin):
    fieldsets = [
        # (None, {'fields': ['question_text']}),
        # ('Date information',
        # {'fields': ['pub_date'], 'classes': ['collapse']}),
    ]
    # list_display = []
    # inlines = [ChoiceInline]


class SchoolInfoAdmin(admin.ModelAdmin):
    fieldsets = [
        # (None, {'fields': ['question_text']}),
        # ('Date information',
        # {'fields': ['pub_date'], 'classes': ['collapse']}),
    ]
    # list_display = []
    # inlines = [ChoiceInline]


class CommonSettingsAdmin(admin.ModelAdmin):
    fieldsets = [
        # (None, {'fields': ['question_text']}),
        # ('Date information',
        # {'fields': ['pub_date'], 'classes': ['collapse']}),
    ]
    # list_display = []
    # inlines = [ChoiceInline]


admin.site.register(ClassRoom, ClassRoomAdmin)
admin.site.register(ContactUs, ContactUsAdmin)
admin.site.register(Customiz, CustomizAdmin)
admin.site.register(SchoolInfo, SchoolInfoAdmin)
admin.site.register(CommonSettings, CommonSettingsAdmin)
