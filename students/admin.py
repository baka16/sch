from django.contrib import admin

# Register your models here.
from .models import *


class AdmissionAdmin(admin.ModelAdmin):

    fieldsets = [
        # (None, {'fields': ['question_text']}),
        # ('Date information',
        # {'fields': ['pub_date'], 'classes': ['collapse']}),
    ]
    # list_display = ['__all__']
    # 'RegNo','first_name','last_name','gender','DoR','academic_year','updated','timestamp',]
    # inlines = [ChoiceInline]


class PerformanceAdmin(admin.ModelAdmin):
    fieldsets = (
        # (None, {
        #     "fields": (
        #         'subject',
        #         'student_regno',
        #         'academic_year',
        #         'term',
        #         'raw_class_score',
        #         'converted_class_score',
        #         'raw_exam_score',
        #         'converted_exam_score',
        #         'grade',
        #         'status',
        #         'comment',
        #         'updated',
        #         'timestamp',
        #     ),
        # }),
    )
    list_display = ['subject',
                    'stid',
                    'academic_year',
                    'term',
                    'raw_class_score',
                    'raw_exam_score',
                    'status',
                    'comment',
                    'updated',
                    'timestamp', ]
    ordering = ['-academic_year']


admin.site.register(Admission, AdmissionAdmin)
admin.site.register(Performance, PerformanceAdmin)
admin.site.register(StudentSugestionsBox)
admin.site.register(TerminalExam)
admin.site.register(MidTermExam)
admin.site.register(ClassTest)
admin.site.register(ClassAssigment)
admin.site.register(ClassExercise)
admin.site.register(MarksConvertions)
admin.site.register(ComplainDesk)


# from django.contrib import admin
# # Specialize the multi-db admin objects for use with specific models.
# class BookInline(MultiDBTabularInline):
# model = Book
# class PublisherAdmin(MultiDBModelAdmin):
# inlines = [BookInline]
# admin.site.register(Author, MultiDBModelAdmin)
# admin.site.register(Publisher, PublisherAdmin)
# othersite = admin.AdminSite('othersite')
# othersite.register(Publisher, MultiDBModelAdmin)
