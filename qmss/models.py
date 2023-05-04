from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.conf import settings
import os

# Create your models here.
class TeacherExtra (models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.user.first_name

    @property
    def get_id(self):
        return self.user.id

    @property
    def get_name(self):
        return self.user.first_name + " " + self.user.last_name



class StaffExtra(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    status = models.BooleanField(default = False)

    @property
    def get_id(self):
        return self.user.id

    @property
    def get_name(self):
        return self.user.first_name + " " + self.user.last_name
    



class StudentExtra (models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    roll_number = models.CharField(max_length=20)
    status = models.BooleanField(default=False)

    @property
    def get_name(self):
        return self.user.first_name + " " + self.user.last_name

    @property
    def get_id(self):
        return self.user.id

    def __str__(self):
        return self.user.first_name
    
class PDFFile(models.Model):
    sender = models.ForeignKey(User,on_delete=models.CASCADE,related_name='pdf_files_sent')
    subject = models.CharField(max_length=200)
    pdf_file = models.FileField(upload_to='pdf_files/%Y/%m/%d')
    created_at = models.DateTimeField(auto_now_add=True)

    def file_url(self):
        return os.path.join(settings.MEDIA_URL, str(self.file))

class Permission_pdf(models.Model):
    shared_object = models.ForeignKey(PDFFile,on_delete=models.CASCADE,related_name='permissions')
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='shared_objects')
    status = models.IntegerField(default=0)






# class Pdf(models.Model):
#     name = models.CharField(max_length=100)
#     file = models.FileField(upload_to='pdfs')
#     viewed = models.BooleanField(default=False)
#     timestamp = models.DateTimeField(auto_now_add=True)
#     approved = models.BooleanField(default=False)
#     uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE,related_name='uploaded_pdfs')
#     tagged_teachers = models.ManyToManyField(User,related_name='tagged_pdfs')

# class Signature(models.Model):
#     pdf = models.ForeignKey(Pdf, on_delete=models.CASCADE)
#     signature = models.FileField(upload_to='signatures')
#     approved = models.BooleanField(default=False)
#     teacher = models.ForeignKey(User, on_delete=models.CASCADE)
