from __future__ import unicode_literals

from django.conf import settings
from django.db import models

from common.common.models import AuditTrailCreatedUpdatedMixin, ActiveMixin, BaseDocumentMixin, QRCodeMixin, NameMixin
from common.course.models import Term, Subject
from common.school.models import AcademicClass


class Student(AuditTrailCreatedUpdatedMixin, ActiveMixin, QRCodeMixin):
    """

    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='stud_crd_by')
    created_date_time = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='stud_upd_by')
    updated_date_time = models.DateTimeField(auto_now_add=True)


class AcademicClassStudent(ActiveMixin, QRCodeMixin):
    student = models.OneToOneField(Student, unique=True)
    academic_class = models.ForeignKey(AcademicClass)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='acd_cls_stud_crd_by')
    created_date_time = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='acd_cls_stud_upd_by')
    updated_date_time = models.DateTimeField(auto_now_add=True)


class StudentSubscription(NameMixin, ActiveMixin):
    academic_class_student = models.ForeignKey(AcademicClassStudent)
    start_date = models.DateField()
    end_date = models.DateField()
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='stud_subscr_crd_by')
    created_date_time = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='stud_subscr_upd_by')
    updated_date_time = models.DateTimeField(auto_now_add=True)


class StudentTermPerformance(ActiveMixin, QRCodeMixin):
    term = models.ForeignKey(Term)
    academic_class_student = models.ForeignKey(AcademicClassStudent)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='term_perf_crd_by')
    created_date_time = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='term_perf_upd_by')
    updated_date_time = models.DateTimeField(auto_now_add=True)


class StudentTermSubjectPerformance(ActiveMixin, QRCodeMixin):
    subject = models.ForeignKey(Subject)
    marks = models.DecimalField(decimal_places=3, max_digits=3)
    student_term = models.ForeignKey(StudentTermPerformance)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='term_sub_perf_crd_by')
    created_date_time = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='term_sub_perf_upd_by')
    updated_date_time = models.DateTimeField(auto_now_add=True)


class StudentDocument(BaseDocumentMixin):
    """

    """
    academic_class_student = models.ForeignKey(AcademicClassStudent)
