from __future__ import unicode_literals

import StringIO

from django.conf import settings
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import models

import qrcode


class BaseModel(models.Model):
    """

    """
    def populate_values(self, exclude=None):
        """
        Method that tries to populate values for fields that are dependent on other fields.
        Returns:

        """
        if exclude is None:
            exclude = []

        for field in self._meta.fields:
            if field.name in exclude:
                continue

            # Get populate function for the field and call it.
            populate_func = getattr(self, 'populate_{}'.format(field.attrname), None)
            if not populate_func:
                continue

            populate_func(field)

    def save(self, *args, **kwargs):
        """
        Calls the methods to dynamically populate field values and saves the data
        Args:
            *args:
            **kwargs:

        Returns:

        """
        self.populate_values()
        super(BaseModel, self).save(*args, **kwargs)

    class Meta:
        abstract = True


class AuditTrailCreatedMixin(BaseModel):
    """

    """
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='created_by')
    created_date_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class AuditTrailUpdatedMixin(BaseModel):
    """

    """
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='updated_by')
    updated_date_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class AuditTrailCreatedUpdatedMixin(AuditTrailCreatedMixin, AuditTrailUpdatedMixin):
    """

    """

    class Meta:
        abstract = True


class ActiveMixin(BaseModel):
    """

    """
    active = models.BooleanField(default=False)

    class Meta:
        abstract = True


class NameMixin(BaseModel):
    """

    """
    name = models.CharField(max_length=50)

    class Meta:
        abstract = True


class AuditTrailActiveNameMixin(NameMixin, ActiveMixin, AuditTrailCreatedUpdatedMixin):
    """

    """
    class Meta:
        abstract = True


class BaseDocumentMixin(BaseModel):
    """

    """
    mongo_id = models.CharField(max_length=100)
    document_type = models.CharField(max_length=10)

    class Meta:
        abstract = True


class QRCodeMixin(BaseModel):
    """
        QRCODE_COMBINATION_FIELDS - List of fields that generator uses to generate QR code
        QRCODE_COMBINATION_SEPARATOR - Separator for QRCODE combination Text
    """
    qr_code_text = models.CharField(max_length=200)
    qr_code_img = models.ImageField(upload_to=settings.UPLOAD_TO_TENANT_DIR)
    qr_code_url_text = models.URLField(max_length=200, blank=True, null=True)
    qr_code_url_img = models.ImageField(upload_to=settings.UPLOAD_TO_TENANT_DIR, blank=True, null=True)

    QRCODE_TEXT_COMBINATION_FIELDS = []
    QRCODE_COMBINATION_SEPARATOR = '-'

    class Meta:
        abstract = True

    # TODO: To be made async
    def generate_qr_code(self, data, field):
        """

        """
        qrcode_img = qrcode.QRCode(version=1,
                                   error_correction=qrcode.constants.ERROR_CORRECT_L,)
        qrcode_img.add_data(data)
        qrcode_img.make(fit=True)
        img = qrcode_img.make_image()
        buffer = StringIO.StringIO()
        img.save(buffer)

        filename = '{}.png'.format(data)
        file_buffer = InMemoryUploadedFile(buffer, None, filename, 'image/png', buffer.len, None)
        field.save(filename, file_buffer)

    def populate_qr_code_text(self, field):
        """

        Returns:

        """
        combination_fields = getattr(self, 'QRCODE_COMBINATION_FIELDS', None)

        combination_sep = getattr(self, 'QRCODE_COMBINATION_FIELDS', None)
        if not combination_fields or not combination_sep:
            raise ValueError('Model attributes QRCODE_COMBINATION_FIELDS, QRCODE_COMBINATION_FIELDS must be set')

        combination_values = map(lambda f: getattr(self, f, ''), combination_fields)
        setattr(self, field.attrname, '{}'.format(combination_sep).join(combination_values))

    def populate_qr_code_img(self, field):
        """

        Returns:

        """
        qr_code_text = getattr(self, 'qr_code_text', None)
        if not qr_code_text:
            return

        self.generate_qr_code(qr_code_text, field)

    def populate_qr_code_url_text(self, field):
        """

        Returns:

        """
        setattr(self, field.attrname, self.get_absolute_url())

    def populate_qr_code_url_img(self, field):
        """

        Returns:

        """
        qr_code_url_text = getattr(self, 'qr_code_url_text', None)
        if not qr_code_url_text:
            return

        self.generate_qr_code(qr_code_url_text, field)
