from __future__ import unicode_literals

from django.conf import settings
from django.db import models

from common.common.models import BaseDocumentMixin, ActiveMixin, QRCodeMixin
from common.school.models import AcademicYear, AcademicClass


class Employee(ActiveMixin, QRCodeMixin):
    """

    """
    employee_type = models.CharField(max_length=1)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='emp_crd_by')
    created_date_time = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='emp_upd_by')
    updated_date_time = models.DateTimeField(auto_now_add=True)


class AcademicEmployee( ActiveMixin, QRCodeMixin):
    employee = models.ForeignKey(Employee)
    academic_year = models.ForeignKey(AcademicYear)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='emp_acad_crd_by')
    created_date_time = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='emp_acad_upd_by')
    updated_date_time = models.DateTimeField(auto_now_add=True)


class AcademicClassEmployee(ActiveMixin, QRCodeMixin):
    employee = models.ForeignKey(Employee)
    academic_class = models.ForeignKey(AcademicClass)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='emp_acad_cls_crd_by')
    created_date_time = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='emp_acad_cls_upd_by')
    updated_date_time = models.DateTimeField(auto_now_add=True)


class EmployeeSubject(ActiveMixin):
    """

    """
    academic_employee = models.ForeignKey(AcademicEmployee)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='emp_sub_crd_by')
    created_date_time = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='emp_sub_upd_by')
    updated_date_time = models.DateTimeField(auto_now_add=True)


class EmployeeClass(ActiveMixin):
    """
    """
    academic_class_employee = models.ForeignKey(AcademicClass)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='emp_cls_crd_by')
    created_date_time = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='emp_cls_upd_by')
    updated_date_time = models.DateTimeField(auto_now_add=True)


class EmployeeDocument(BaseDocumentMixin):
    academic_employee = models.ForeignKey(AcademicEmployee)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='emp_doc_crd_by')
    created_date_time = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='emp_doc_upd_by')
    updated_date_time = models.DateTimeField(auto_now_add=True)
