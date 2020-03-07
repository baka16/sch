from django.conf import settings
from django.contrib.postgres.fields import ArrayField, JSONField
from django.db import models

from .models import AuditTrailCreatedUpdatedMixin, NameMixin


class ReferenceChoice(NameMixin):
    """

    """
    choices = JSONField()
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='ref_choice_crd_by')
    created_date_time = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='ref_choice_upd_by')
    updated_date_time = models.DateTimeField(auto_now_add=True)


class ReferenceFacility(NameMixin):
    """

    """
    data = JSONField()
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='ref_facility_crd_by')
    created_date_time = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='ref_facility_upd_by')
    updated_date_time = models.DateTimeField(auto_now_add=True)


class ReferenceItem(NameMixin):
    """

    """
    data = ArrayField(models.CharField(max_length=30))
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='ref_item_crd_by')
    created_date_time = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='ref_item_upd_by')
    updated_date_time = models.DateTimeField(auto_now_add=True)


class ReferenceDepartment(NameMixin):
    """

    """
    descr = models.CharField(max_length=200)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='ref_dept_crd_by')
    created_date_time = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='ref_dept_upd_by')
    updated_date_time = models.DateTimeField(auto_now_add=True)


class ReferenceDesignation(NameMixin):
    """

    """
    descr = models.CharField(max_length=200)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='ref_designation_crd_by')
    created_date_time = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='ref_designation_upd_by')
    updated_date_time = models.DateTimeField(auto_now_add=True)
