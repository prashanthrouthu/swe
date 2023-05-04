from django import forms
from django.contrib.auth.models import User
from . import models
from .models import StaffExtra,StudentExtra,TeacherExtra, PDFFile, Permission_pdf
from django_select2.forms import Select2MultipleWidget
# from django_select2.forms import Select2Widget


class StudentExtraform(forms.ModelForm):
    class Meta:
        model = StudentExtra
        fields = ['roll_number']

class TeacherExtraform(forms.ModelForm):
    class Meta:
        model = TeacherExtra
        fields = []

class StaffExtraform(forms.ModelForm):
    class Meta:
        model = StaffExtra
        fields = []

# class Pdfform(forms.ModelForm):
#     class Meta:
#         model = models.Pdf
#         fields = ['name','file']

class AdminSignupForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required = True
    class Meta:
        model = User
        fields = ['email','first_name', 'last_name', 'username', 'password']



class StudentUserForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required = True
    class Meta:
        model = User
        fields = ['email','first_name', 'last_name', 'username', 'password']


class TeacherUserForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required = True
    class Meta:
        model = User
        fields = ['email','first_name', 'last_name', 'username', 'password']


class StaffUserForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required = True
    class Meta:
        model = User
        fields = ['email','first_name', 'last_name', 'username', 'password']

class PDFFileform(forms.ModelForm):
    class Meta:
        model = PDFFile
        fields = ['subject','pdf_file']

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['pdf_file'].widget.attrs.update({'accept': '.pdf'})

    def save(self,sender):
        pdffile=super().save(commit=False)
        pdffile.sender= sender
        pdffile.save()
        return pdffile
    

class permissions_form(forms.Form):
    email = forms.EmailField()






# class give_permission(forms.ModelForm):
#     class Meta:
#         model = User
#         fields =['email']

# class Sharedobjectform(forms.Modelform):
#     recipients= forms.ModelMultipleChoiceField(
#         queryset= User.objects.all(),
#         widget = Select2MultipleWidget(atrrs={'dataplaceholder': 'search and select recipients'})
#     )
#     class Meta:
#         model = Permission_pdf
#         fields={'object','recipients'}
        






        