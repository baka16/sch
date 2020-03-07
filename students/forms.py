from django import forms

from .models import Admission, Performance

# from helper import helpers, utils, validators


class AdmissionCreateForm(forms.ModelForm):
    class Meta:
        model = Admission
        # fields = ['__all__'
        #     'first_name', 'last_name', 'gender',
        #     'passport','date_of_birth',
        #     'health_issue','academic_year','term','disabled',
        #     'disability_details','languages',
        #     'level','class_enroll','house',
        #     'comment',
        # ]
        exclude = ['admitted_by', 'update', 'timestamp']

        # first_name = forms.CharField(required=False)
        # last_name = forms.CharField(required=False)
        # gender = forms.CharField(required=False)
        # comment = forms.CharField(required=False)


class PerformanceCreateForm(forms.ModelForm):
    class Meta:
        model = Performance
        fields = '__all__'
        # 'subject',
        # 'academic_year',
        # 'term',
        # 'raw_class_score',
        # # 'converted_class_score',
        # 'raw_exam_score',
        # # 'converted_exam_score',
        # # 'grade',
        # 'status',
        # 'comment',
