from django import forms
from django.utils.translation import ugettext_lazy as _
from .models import ClassRoom, ContactUs


class ClassRoomCreateForm(forms.ModelForm):
    # <div class="input-group">
	# 	<input class="form-control date-picker" id="id-date-picker-1" type="text" data-date-format="dd-mm-yyyy">
    #     <span class="input-group-addon"><i class="fa fa-calendar bigger-110"></i></span></div>
        
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}) )

    class Meta:
        model = ClassRoom
        exclude = ['update','timestamp']


class ContactForm(forms.Form):
    # name = forms.CharField(_('Name'))
    # forms.EmailField(_('Email'), required=False)
    # message = forms.CharField(_('Message'), widget=forms.Textarea)

     # name = forms.CharField(max_length = 50, required = True, widget=forms.TextInput()
    #    attrs = {'class':'form-control','placeholder':'name'},
    #    error_messages = {'required' : "This field is required",'invalid' : "This field is invalid"},
    #    )
    class Meta:
        model = ContactUs
        exclude = ['update','timestamp']


    def send_email(self):
        # send email using the self.cleaned_data dictionary
        pass

    def clean(self):
        cleaned_data = super().clean()
        #Do Stuff
        