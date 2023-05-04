from django.contrib import admin

# Register your models here.
from qmss.models import TeacherExtra, StudentExtra,PDFFile   #, Pdf

admin.site.register(TeacherExtra)
admin.site.register(StudentExtra)
admin.site.register(PDFFile)
# admin.site.register(Pdf)
