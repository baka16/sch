from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models

from common.common import constants
from common.common.models import AuditTrailCreatedUpdatedMixin, QRCodeMixin, ActiveMixin


class ExtendedUser(AbstractUser, QRCodeMixin):
    """

    """
    mobile_number = models.IntegerField()
    alternate_number = models.IntegerField()
    country_code = models.IntegerField(default=91)
    alternate_country_code = models.IntegerField(default=91)
    dob = models.DateField()
    gender = models.CharField(max_length=1, choices=constants.GENDER_CHOICES)
    photo = models.ImageField(upload_to=settings.UPLOAD_AVATARS_TO)
    blood_group = models.CharField(max_length=10, choices=constants.BLOOD_GROUP_CHOICES)
    user_type = models.CharField(max_length=1, choices=constants.USER_TYPE_CHOICES)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user_created_by')
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user_updated_by')


class Address(ActiveMixin):
    """

    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    line_1 = models.CharField(max_length=100)
    line_2 = models.CharField(max_length=100)
    city = models.CharField(max_length=30)
    state = models.CharField(max_length=30)
    country = models.CharField(max_length=30)
    zip_code = models.IntegerField()
    address_type = models.CharField(max_length=1, choices=constants.ADDRESS_TYPE_CHOICES)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='address_crd_by')
    created_date_time = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='address_upd_by')
    updated_date_time = models.DateTimeField(auto_now_add=True)


class PhoneNumber(AuditTrailCreatedUpdatedMixin, ActiveMixin):
    """

    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    phone_connection_type = models.CharField(max_length=1, choices=constants.PHONE_CONNECTION_TYPE_CHOICES)
    country_code = models.IntegerField(default=91)
    area_code = models.IntegerField()
    phone_number = models.IntegerField()
    phone_number_type = models.CharField(max_length=1, choices=constants.PHONE_NUMBER_TYPE_CHOICES)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='phone_crd_by')
    created_date_time = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='phone_upd_by')
    updated_date_time = models.DateTimeField(auto_now_add=True)
