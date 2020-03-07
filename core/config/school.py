from __future__ import unicode_literals

from django.conf import settings
from django.db import models

# Create your models here.
from common.common.models import NameMixin, AuditTrailCreatedUpdatedMixin, QRCodeMixin, BaseDocumentMixin, ActiveMixin, AuditTrailActiveNameMixin


class School(NameMixin, QRCodeMixin):
    """

    """
    established_year = models.IntegerField()
    logo = models.ImageField()
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='sch_crd_by')
    created_date_time = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='sch_perf_upd_by')
    updated_date_time = models.DateTimeField(auto_now_add=True)


class SchoolAdministration(NameMixin, QRCodeMixin):
    """

    """
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='sch_adm_crd_by')
    created_date_time = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='sch_adm_upd_by')
    updated_date_time = models.DateTimeField(auto_now_add=True)


class SchoolDocument(BaseDocumentMixin):
    school = models.ForeignKey(School)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='sch_doc_crd_by')
    created_date_time = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='sch_doc_upd_by')
    updated_date_time = models.DateTimeField(auto_now_add=True)


class AcademicYear(ActiveMixin, QRCodeMixin):
    """

    """
    start_year = models.IntegerField()
    end_year = models.IntegerField()
    start_month = models.CharField(max_length=3)
    end_month = models.CharField(max_length=3)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='acd_year_crd_by')
    created_date_time = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='acd_year_upd_by')
    updated_date_time = models.DateTimeField(auto_now_add=True)


class AcademicClass(NameMixin, ActiveMixin, QRCodeMixin):
    academic_year = models.ForeignKey(AcademicYear)
    standard = models.CharField(max_length=10)
    section = models.CharField(max_length=10)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='acd_cls_crd_by')
    created_date_time = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='acd_cls_upd_by')
    updated_date_time = models.DateTimeField(auto_now_add=True)
