# from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import post_save, pre_save
from django.urls import reverse
from django.utils import dateparse, timezone
from django.utils.translation import gettext_lazy as _

from . import studentmanager
from aids.models import ClassRoom
from helper import helpers, utils, validators

User = get_user_model()
# settings.AUTH_USER_MODEL
app_name = 'student'


def get_for_replace_user():
    return get_user_model().objects.get_or_create(username='deleted')[0]


class Admission(models.Model):
    RegNo = models.CharField('Registration Number', max_length=15, validators=[
                             validators.student_reg_num])
    stid = models.CharField(
        'Student Unique ID', max_length=18, unique=True, validators=[validators.stid])
    first_name = models.CharField('First Name', max_length=40)
    last_name = models.CharField('Last Name(s)', max_length=40)
    gender = models.CharField("Gender", max_length=7,
                              choices=helpers.GENDER, default="Female")
    passport = models.FileField(
        'Passport Image', upload_to='passports/students', blank=True, default="default.png")
    DoR = models.DateField('Date of Registration',
                           null=True, default=timezone.now)
    date_of_birth = models.DateField(
        auto_now=False, auto_now_add=False, null=True, blank=True)
    health_issue = models.BooleanField('Any Health Issue', default=False)
    academic_year = models.CharField(
        'Academic Year', max_length=20, choices=helpers.AC_YEARS)
    term = models.CharField('Term', max_length=10,
                            choices=helpers.TERMS_LIST_NUMERIC, default='1')
    disabled = models.BooleanField('Disabled', default=False)
    disability_details = models.CharField(
        'Disability Details', max_length=100, default='NILL')
    languages = models.CharField(
        'Language Spoken', max_length=100, null=True, blank=True)
    religion = models.CharField(
        'Religion', max_length=100, choices=helpers.RELIGION, null=True, blank=True)

    level = models.CharField('Level', max_length=20, choices=helpers.LEVELS)
    class_enroll = models.ForeignKey(ClassRoom, on_delete=models.SET_NULL,
                                     null=True, blank=True, to_field='id', verbose_name="Class Enroll")
    # class_enroll  = models.CharField( 'Class', max_length=20, choices=helpers.CLASSES, default='PRIMARY ONE')
    house = models.CharField('House/Compound', max_length=20, null=True,
                             blank=True, choices=helpers.HOUSES, default='NOT ASSIGNED')

    gurdian_name = models.CharField('Guardian Name', max_length=50,)
    address = models.CharField(
        'Address', max_length=100, null=True, blank=True)
    # religion    = models.CharField('Religion',max_length=100,choices=helpers.RELIGION,null=True, blank=True)
    phone = models.CharField(' Contact', max_length=100, null=True, blank=True)
    email = models.EmailField(' Email', max_length=50, null=True, blank=True)
    # address= models.CharField('parent Address',max_length=100, null=True, blank=True)

    father_name = models.CharField('Fathers Name', max_length=50,)
    father_hometown = models.CharField('Fathers Hometown', max_length=50,)
    father_phone = models.CharField(
        'Fathers Contact', max_length=30, blank=True)
    mother_name = models.CharField('Mothers Name', max_length=50, )
    mother_phone = models.CharField(
        'Mothers Contact', max_length=30, blank=True)

    admitted_by = models.ForeignKey(User, verbose_name=_(
        "Admitted By"), on_delete=models.SET(get_for_replace_user),)
    comment = models.TextField(
        _("Comment"), max_length=100, null=True, blank=True)
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    # objects = AdmissionManager()
    objects = studentmanager.AdmissionManager()

    class Meta:
        verbose_name = 'Admission'
        verbose_name_plural = 'Admissions'
        ordering = ['-academic_year', '-updated', '-timestamp']

    def __str__(self):
        return self.title
        # return f"{self.first_nameAdams Alimatu} {self.last_name} "

    def save(self, *args, **kwargs):
        # Call the real save() method
        super(Admission, self).save(*args, **kwargs)

    def get_absolute_url(self):
        # return f"/student/{self.stid}"
        return reverse('student:details', kwargs={'pk': self.stid})

    # TODO: Define custom methods here
    def get_edit_url(self):
        return f"{self.get_absolute_url()}edit"

    def get_delete_url(self):
        return f"{self.get_absolute_url()}delete"

    def get_student_Languages(self):
        return self.languages.split(',')

    @property
    def full_name(self):
        return f" {self.first_name} {self.last_name} "

    @property
    def title(self):
        return self.stid


class StudentSugestionsBox(models.Model):
    """Model definition for Student Sugestions Box."""
    stid = models.ForeignKey(
        Admission, on_delete=models.CASCADE, to_field='stid', verbose_name="Student")
    title = models.CharField(max_length=15,)
    body = models.TextField(_("Suggestion"),)
    category = models.CharField(
        "Suggetion for", max_length=15, choices=helpers.SUGGESTION_CATEGORY)
    status = models.CharField("Sugestion Status", max_length=50, null=True,)
    comment = models.CharField(
        'Comment', max_length=100, null=True, blank=True)
    remarks = models.CharField("Sugestion remarks", max_length=50, null=True,)
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    # TODO: Define fields here

    class Meta:
        verbose_name = 'Student suggestion'
        verbose_name_plural = 'Students suggestions'
        ordering = ['-updated', '-timestamp']

    def __str__(self):
        return f"{self.title} "

    def save(self, *args, **kwargs):
        super(StudentSugestionsBox, self).save(
            *args, **kwargs)  # Call the real save() method

    def get_absolute_url(self):
        return reverse('student:suggestions', kwargs={'pk': self.id})

    # TODO: Define custom methods here
    def get_edit_url(self):
        return f"{self.get_absolute_url()}/edit"

    def get_delete_url(self):
        return f"{self.get_absolute_url()}/delete"

    @property
    def title(self):
        return self.title


class Performance(models.Model):
    """Model definition for Performance."""
    subject = models.CharField(
        "Subject", max_length=50, choices=helpers.SUBJECTS_LIST)
    stid = models.ForeignKey(
        Admission, on_delete=models.CASCADE, to_field='stid', verbose_name="Student")
    # student_name  = models.ForeignKey(Student.full_name, on_delete=models.CASCADE)
    academic_year = models.CharField(
        'Academic Year', max_length=20, choices=helpers.AC_YEARS, default='1999/1999')
    term = models.CharField("Term", max_length=15,
                            choices=helpers.TERMS_LIST_NUMERIC)
    raw_class_score = models.FloatField("Raw Class Score")
    # converted_class_score = models.FloatField("Converted Class Score")
    raw_exam_score = models.FloatField("Raw Exams Score")
    # converted_exam_score  = models.FloatField("Converted Exams Score")
    # grade  = models.CharField("Subject Grade", max_length=15)
    status = models.CharField("Performance Status", max_length=15)
    comment = models.CharField(
        'Comment', max_length=100, null=True, blank=True)
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    # TODO: Define fields here

    class Meta:
        verbose_name = 'Performance'
        verbose_name_plural = 'Performances'
        ordering = ['-academic_year', '-updated', '-timestamp']

    def __str__(self):
        return f"{self.stid} Results for {self.subject} "

    def save(self, *args, **kwargs):
        # Call the real save() method
        super(Performance, self).save(*args, **kwargs)

    def get_absolute_url(self):
        # return f"/student/details/{self.stid}"
        return reverse('student:performance', kwargs={'pk': self.stid})

    # TODO: Define custom methods here
    def get_edit_url(self):
        return f"{self.get_absolute_url()}/edit"

    def get_delete_url(self):
        return f"{self.get_absolute_url()}/delete"


class TerminalExam(models.Model):
    subject = models.CharField(
        "Subject", max_length=50, choices=helpers.SUBJECTS_LIST)
    stid = models.ForeignKey(
        Admission, on_delete=models.CASCADE, to_field='stid', verbose_name="Student code")
    # student_name    = models.ForeignKey('self'.full_name, on_delete=models.CASCADE)
    academic_year = models.CharField(
        'Academic Year', max_length=20, choices=helpers.AC_YEARS, default='1999/1999')
    term = models.CharField("Term", max_length=2,
                            choices=helpers.TERMS_LIST_NUMERIC)
    raw_score = models.DecimalField(
        'Raw score', max_digits=4, decimal_places=2)
    total_marks = models.PositiveSmallIntegerField('Total Mark', )
    status = models.CharField("Performance Status", max_length=15)
    comment = models.CharField('Comment', max_length=100,)
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Terminal Examination'
        verbose_name_plural = 'Terminal Examinations'
        ordering = ['term', 'raw_score',
                    '-academic_year', '-updated', '-timestamp']

    def __str__(self):
        return f"Results for {self.subject} "

    def save(self, *args, **kwargs):
        # Call the real save() method
        super(TerminalExam, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('student:terminal-exam', kwargs={'pk': self.id})

    def get_edit_url(self):
        return f"{self.get_absolute_url()}/edit"

    def get_delete_url(self):
        return f"{self.get_absolute_url()}/delete"

    @property
    def full_name(self):
        return Admission.full_name


class MidTermExam(models.Model):
    subject = models.CharField(
        "Subject", max_length=50, choices=helpers.SUBJECTS_LIST)
    stid = models.ForeignKey(
        Admission, on_delete=models.CASCADE, to_field='stid', verbose_name="Student code")
    # student_name    = models.ForeignKey(Student.full_name, on_delete=models.CASCADE)
    academic_year = models.CharField(
        'Academic Year', max_length=20, choices=helpers.AC_YEARS, default='1999/1999')
    term = models.CharField("Term", max_length=2,
                            choices=helpers.TERMS_LIST_NUMERIC)
    raw_score = models.DecimalField(
        'Raw score', max_digits=4, decimal_places=2)
    total_marks = models.PositiveSmallIntegerField('Total Mark',)
    status = models.CharField("Performance Status", max_length=15)
    comment = models.CharField('Comment', max_length=100,)
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Mid-Term Examination'
        verbose_name_plural = 'Mid-Term Examinations'
        ordering = ['term', 'raw_score',
                    '-academic_year', '-updated', '-timestamp']

    def __str__(self):
        return f"Results for {self.subject} "

    def save(self, *args, **kwargs):
        # Call the real save() method
        super(MidTermExam, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('student:mid-term-exam', kwargs={'pk': self.id})

    def get_edit_url(self):
        return f"{self.get_absolute_url()}/edit"

    def get_delete_url(self):
        return f"{self.get_absolute_url()}/delete"


class ClassTest(models.Model):
    subject = models.CharField(
        "Subject", max_length=50, choices=helpers.SUBJECTS_LIST)
    stid = models.ForeignKey(
        Admission, on_delete=models.CASCADE, to_field='stid', verbose_name="Student code")
    # student_name    = models.ForeignKey(Student.full_name, on_delete=models.CASCADE)
    academic_year = models.CharField(
        'Academic Year', max_length=20, choices=helpers.AC_YEARS, default='1999/1999')
    term = models.CharField("Term", max_length=2,
                            choices=helpers.TERMS_LIST_NUMERIC)
    raw_score = models.DecimalField(
        'Raw score', max_digits=4, decimal_places=2)
    total_marks = models.PositiveSmallIntegerField('Total Mark',)
    status = models.CharField("Performance Status", max_length=15)
    comment = models.CharField('Comment', max_length=100,)
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Class Test'
        verbose_name_plural = 'Class Test'
        ordering = ['term', 'raw_score',
                    '-academic_year', '-updated', '-timestamp']

    def __str__(self):
        return f"Results for {self.subject} "

    def save(self, *args, **kwargs):
        # Call the real save() method
        super(ClassTest, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('student:class-test', kwargs={'pk': self.id})

    def get_edit_url(self):
        return f"{self.get_absolute_url()}/edit"

    def get_delete_url(self):
        return f"{self.get_absolute_url()}/delete"


class ClassAssigment(models.Model):
    subject = models.CharField(
        "Subject", max_length=50, choices=helpers.SUBJECTS_LIST)
    stid = models.ForeignKey(
        Admission, on_delete=models.CASCADE, to_field='stid', verbose_name="Student code")
    # student_name    = models.ForeignKey(Student.full_name, on_delete=models.CASCADE)
    academic_year = models.CharField(
        'Academic Year', max_length=20, choices=helpers.AC_YEARS, default='1999/1999')
    term = models.CharField("Term", max_length=2,
                            choices=helpers.TERMS_LIST_NUMERIC)
    raw_score = models.DecimalField(
        'Raw score', max_digits=4, decimal_places=2)
    total_marks = models.PositiveSmallIntegerField('Total Mark',)
    status = models.CharField("Performance Status", max_length=15)
    comment = models.CharField('Comment', max_length=100,)
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Class Assigment'
        verbose_name_plural = 'Class Assigments'
        ordering = ['term', 'raw_score',
                    '-academic_year', '-updated', '-timestamp']

    def __str__(self):
        return f"Results for {self.subject} "

    def save(self, *args, **kwargs):
        super(ClassAssigment, self).save(
            *args, **kwargs)  # Call the real save() method

    def get_absolute_url(self):
        return reverse('student:class-test', kwargs={'pk': self.id})

    def get_edit_url(self):
        return f"{self.get_absolute_url()}/edit"

    def get_delete_url(self):
        return f"{self.get_absolute_url()}/delete"


class ClassExercise(models.Model):
    subject = models.CharField(
        "Subject", max_length=50, choices=helpers.SUBJECTS_LIST)
    stid = models.ForeignKey(
        Admission, on_delete=models.CASCADE, to_field='stid', verbose_name="Student code")
    # student_name    = models.ForeignKey(Student.full_name, on_delete=models.CASCADE)
    academic_year = models.CharField(
        'Academic Year', max_length=20, choices=helpers.AC_YEARS, default='1999/1999')
    term = models.CharField("Term", max_length=2,
                            choices=helpers.TERMS_LIST_NUMERIC)
    raw_score = models.DecimalField(
        'Raw score', max_digits=4, decimal_places=2)
    total_marks = models.PositiveSmallIntegerField('Total Mark',)
    status = models.CharField("Performance Status", max_length=15)
    comment = models.CharField('Comment', max_length=100,)
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Class Exercise'
        verbose_name_plural = 'Class Exercises'
        ordering = ['term', 'raw_score',
                    '-academic_year', '-updated', '-timestamp']

    def __str__(self):
        return f"Results for {self.subject} "

    def save(self, *args, **kwargs):
        # Call the real save() method
        super(ClassExercise, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('student:class-exercise', kwargs={'pk': self.id})

    def get_edit_url(self):
        return f"{self.get_absolute_url()}/edit"

    def get_delete_url(self):
        return f"{self.get_absolute_url()}/delete"


class MarksConvertions(models.Model):
    exam_type = models.CharField('Exam Type', max_length=50,)
    total_marks = models.PositiveSmallIntegerField('Total Mark', )
    convert_to = models.PositiveSmallIntegerField('Convert score to', )
    comment = models.CharField('Comment', max_length=100,)
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Marks Convertion'
        verbose_name_plural = 'Marks Convertions'
        ordering = ['exam_type', '-updated', '-timestamp']

    def __str__(self):
        return f"{self.exam_type} marks convertion is {self.convert_to} "

    def save(self, *args, **kwargs):
        super(MarksConvertions, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('student:marks-convertions', kwargs={'pk': self.id})

    def get_edit_url(self):
        return f"{self.get_absolute_url()}/edit"

    def get_delete_url(self):
        return f"{self.get_absolute_url()}/delete"


class ComplainDesk(models.Model):
    reason = models.CharField("Complain for", max_length=100)
    details = models.TextField("Complain details",)

    stid = models.CharField('Student Unique ID', max_length=18,)
    student_name = models.CharField('Student name', max_length=70)
    # reason  = models.CharField("Complain for", max_length=100)
    comment = models.CharField('Comment', max_length=100,)
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Complain Desk'
        verbose_name_plural = 'Complains Desk'
        ordering = ['-updated', '-timestamp']

    def __str__(self):
        return f"{self.reason}"

    def save(self, *args, **kwargs):
        super(ComplainDesk, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('student:complains', kwargs={'pk': self.id})

    def get_edit_url(self):
        return f"{self.get_absolute_url()}/edit"

    def get_delete_url(self):
        return f"{self.get_absolute_url()}/delete"
