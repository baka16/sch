from __future__ import unicode_literals

from django.conf import settings
from django.db import models

from common.common.models import (ActiveMixin, NameMixin, QRCodeMixin)
from common.school.models import AcademicYear


class Course(NameMixin, ActiveMixin, QRCodeMixin):
    academic_year = models.ForeignKey(AcademicYear)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='course_crd_by')
    created_date_time = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='course_upd_by')
    updated_date_time = models.DateTimeField(auto_now_add=True)


class Subject(NameMixin, ActiveMixin, QRCodeMixin):
    course = models.ForeignKey(Course)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='sub_crd_by')
    created_date_time = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='sub_upd_by')
    updated_date_time = models.DateTimeField(auto_now_add=True)


class Lesson(NameMixin, ActiveMixin):
    subject = models.ForeignKey(Subject)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='lesson_crd_by')
    created_date_time = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='lesson_upd_by')
    updated_date_time = models.DateTimeField(auto_now_add=True)


class Term(NameMixin, ActiveMixin):
    academic_year = models.ForeignKey(AcademicYear)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='term_crd_by')
    created_date_time = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='term_upd_by')
    updated_date_time = models.DateTimeField(auto_now_add=True)
