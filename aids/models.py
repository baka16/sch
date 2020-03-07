from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from helper import helpers, validators
from helper.utils import unique_slug_generator

#
User = settings.AUTH_USER_MODEL

app_name = 'aids'


class ClassRoom(models.Model):
    name = models.CharField(max_length=20, help_text='Enter Class Name')
    title = models.CharField(max_length=20, help_text='Enter class short name')
    slug = models.SlugField(
        _("Class Slug"), unique=True, help_text='Unique class name without spaces')
    numeric_name = models.CharField(
        max_length=20, help_text='Numeric Class Name')
    comment = models.CharField('Comment', max_length=70, blank=True)
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    # Metadata
    class Meta:
        verbose_name = 'School Class Room'
        verbose_name_plural = 'School Class Rooms'
        ordering = ['-name']

    # Methods
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('aids:classroom', kwargs={'pk': self.slug})
        # return reverse('aids:classroom', args=['title':title])

    def save(self, *args, **kwargs):
        # Call the real save() method
        super(ClassRoom, self).save(*args, **kwargs)

    def get_edit_url(self):
        return f"{self.get_absolute_url()}/edit"

    def get_delete_url(self):
        return f"{self.get_absolute_url()}/delete"


class ContactUs(models.Model):
    """Model definition for Contact Us."""
    name = models.CharField(_("Name"), max_length=50,)
    Email = models.EmailField(_("Email"), max_length=60, blank=True,)
    Message = models.TextField(_("Write your message "), max_length=50,)
    status = models.CharField("Contact status", max_length=15, blank=True,)
    comment = models.CharField('Comment', max_length=100, blank=True)
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    # TODO: Define fields here

    class Meta:
        verbose_name = 'Contact us'
        verbose_name_plural = 'Contact us'
        ordering = ['name', '-updated', '-timestamp']

    def __str__(self):
        return f"{self.name} with email: {self.email} "

    def get_absolute_url(self):
        return reverse('aids:contact', kwargs={'pk': self.id})

    def save(self, *args, **kwargs):
        # Call the real save() method
        super(ContactUs, self).save(*args, **kwargs)

    def get_edit_url(self):
        return f"{self.get_absolute_url()}/edit"

    def get_delete_url(self):
        return f"{self.get_absolute_url()}/delete"


# settings
class Customiz(models.Model):
    """Model definition for Customiz."""
    name = models.CharField("customize Name", max_length=50,)
    value = models.CharField("value", max_length=150,)

    status = models.CharField("Customize Status", max_length=100, blank=True,)
    comment = models.CharField('Comment', max_length=100, blank=True)
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    # TODO: Define fields here

    class Meta:
        verbose_name = 'Customization'
        verbose_name_plural = 'Customizations'
        ordering = ['name', '-updated', '-timestamp']

    def __str__(self):
        return f"{self.name} with value: {self.value} "

    def get_absolute_url(self):
        return reverse('aids:customize', kwargs={'pk': self.id})

    def save(self, *args, **kwargs):
        # Call the real save() method
        super(Customiz, self).save(*args, **kwargs)

    def get_edit_url(self):
        return f"{self.get_absolute_url()}/edit"

    def get_delete_url(self):
        return f"{self.get_absolute_url()}/delete"


class SchoolInfo (models.Model):
    regno = models.CharField('School Registration ID', max_length=20,)
    name = models.CharField(max_length=150, )
    title = models.CharField(max_length=70, )
    school_motor = models.CharField(max_length=300, blank=True,)
    slug = models.SlugField(max_length=150, )
    decription = models.TextField('Describtion')
    mission = models.TextField('School mission ', blank=True,)
    vission = models.TextField('School vission', blank=True,)
    school_open_date = models.DateField(_("School Oppening Date/Year"),)
    logo = models.FileField(
        'Passport Image', upload_to='sch-logo/', blank=True, null=True)
    contact = models.CharField(max_length=70, )
    sms_number = models.CharField(max_length=70, blank=True,)
    GPS_address = models.CharField(
        'School GPS Address', max_length=70, blank=True,)
    postal_address = models.TextField('School Postal Address')
    email = models.EmailField('School Email Address')
    location = models.CharField(max_length=70, )
    website = models.URLField('School website address')
    # category = models.CharField("Term", max_length=15, choices=helpers.SUGGESTION_CATEGORY)
    school_main_color = models.CharField(
        _("School main color"), max_length=15, choices=helpers.MAIN_COLORS)
    status = models.CharField("School Status", max_length=70, blank=True,)
    comment = models.TextField('Comment', blank=True,)
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    # Metadata
    class Meta:
        verbose_name = 'School Information'
        verbose_name_plural = 'School Informations'
        ordering = ['-updated', '-timestamp', 'school_open_date']

    # Methods
    def __str__(self):
        return f"{self.name}"

    def get_absolute_url(self):
        return reverse('aids:schoolinfo', kwargs={'slug': self.slug})
        # return reverse('aids:schoolinfo', args=[args])

    def save(self, *args, **kwargs):
        # Call the real save() method
        super(SchoolInfo, self).save(*args, **kwargs)

    def get_edit_url(self):
        return f"{self.get_absolute_url()}/edit"

    def get_delete_url(self):
        return f"{self.get_absolute_url()}/delete"


class CommonSettings (models.Model):
    name = models.CharField(max_length=150, )
    value = models.CharField(max_length=150, )
    decription = models.TextField('Describtion', blank=True,)
    comment = models.TextField('Comment', blank=True,)
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    # Metadata
    class Meta:
        verbose_name = 'School Common Setting'
        verbose_name_plural = 'School Common Settings'
        ordering = ['name', '-updated', '-timestamp']

    # Methods

    def __str__(self):
        return f"{self.name} with value: {self.value} "

    def get_absolute_url(self):
        return reverse('aids:CommonSettings', kwargs={'pk': self.id})

    def save(self, *args, **kwargs):
        super(CommonSettings, self).save(
            *args, **kwargs)  # Call the real save() method

    def get_edit_url(self):
        return f"{self.get_absolute_url()}/edit"

    def get_delete_url(self):
        return f"{self.get_absolute_url()}/delete"
