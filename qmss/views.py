from django.shortcuts import render, redirect, reverse
from . import forms
from . import models
# from .forms import StudentExtraform
from django.http import HttpResponseRedirect, Http404
from django.db.models import Sum
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required, user_passes_test
from django.conf import settings
import os


# Create your views here.
def base(request):
    return render(request,'qmss/index.html')

def index(request):
    """The home page for qmss"""
    return render(request,'qmss/index.html')

def adminclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect ('afterlogin')
    return render (request, 'qmss/adminclick.html')

def teacherclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect ('afterlogin')
    return render (request, 'qmss/teacherclick.html')

def staffclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect ('afterlogin')
    return render (request, 'qmss/staffclick.html')


def studentclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render (request, 'qmss/studentclick.html')


def admin_signup_view(request):
    if request.method == 'POST':
        form = forms.AdminSignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.set_password(user.password)
            user.save()

            my_admin_group = Group.objects.get_or_create(name='ADMIN')
            my_admin_group[0].user_set.add(user)
            return HttpResponseRedirect('adminlogin')
    else:
        form = forms.AdminSignupForm()
    context ={'form':form}
    return render (request, 'qmss/adminsignup.html', context)


def student_signup_view(request):
    if request.method == 'POST':
        form1 = forms.StudentUserForm(request.POST)
        form2 = forms.StudentExtraform(request.POST)
        if form1.is_valid() and form2.is_valid():
            user = form1.save()
            user.set_password(user.password)
            user.save()
            f2 = form2.save(commit=False)
            f2.user = user
            user2 = f2.save()

            my_student_group = Group.objects.get_or_create (name='STUDENT')
            my_student_group[0].user_set.add (user)
            return HttpResponseRedirect ('studentlogin')
    else:
        form1 = forms.StudentUserForm()
        form2 = forms.StudentExtraform()

    context = {'form1': form1, 'form2': form2}
    return render (request, 'qmss/studentsignup.html', context)


def teacher_signup_view(request):

    if request.method == 'POST':
        form1 = forms.TeacherUserForm(request.POST)
        form2 = forms.TeacherExtraform(request.POST)
        if form1.is_valid() and form2.is_valid():
            user = form1.save()
            user.set_password(user.password)
            user.save()
            f2 = form2.save(commit=False)
            f2.user = user
            user2 = f2.save()

            my_teacher_group = Group.objects.get_or_create(name='TEACHER')
            my_teacher_group[0].user_set.add(user)
            return HttpResponseRedirect('teacherlogin')
    else:
        form1 = forms.TeacherUserForm()
        form2 = forms.TeacherExtraform()
    context={'form1': form1, 'form2': form2}
    return render(request, 'qmss/teachersignup.html', context)

def staff_signup_view(request):
    if request.method == 'POST':
        form1 = forms.StaffUserForm(request.POST)
        form2 = forms.StaffExtraform(request.POST)
        if form1.is_valid() and form2.is_valid():
            user = form1.save()
            user.set_password(user.password)
            user.save()
            f2 = form2.save(commit=False)
            f2.user = user
            user2 = f2.save()
            my_staff_group = Group.objects.get_or_create(name='STAFF')
            my_staff_group[0].user_set.add(user)
            return HttpResponseRedirect('stafflogin')
    else:
        form1 = forms.StaffUserForm()
        form2 = forms.StaffExtraform()
    context={'form1': form1, 'form2': form2}
    return render(request, 'qmss/staffsignup.html', context)


def is_admin(user):
    return user.groups.filter(name='ADMIN').exists()


def is_teacher(user):
    return user.groups.filter(name='TEACHER').exists()


def is_student(user):
    return user.groups.filter(name='STUDENT').exists()

def is_staff(user):
    return user.groups.filter(name='STAFF').exists()


def afterlogin_view(request):
    if is_admin(request.user):
        return admindashboardview(request)
    elif is_teacher(request.user):
        accountapproval = models.TeacherExtra.objects.all().filter(user_id=request.user.id, status=True)
        if accountapproval:
            return teacherdashboardview(request)
        else:
            return render(request, 'qmss/teacher_wait_for_approval.html')
    elif is_student(request.user):
        accountapproval = models.StudentExtra.objects.all().filter(user_id=request.user.id, status=True)
        if accountapproval:
            return studentdashboardview(request)
        else:
            return render(request, 'qmss/student_wait_for_approval.html')
    elif is_staff(request.user):
        accountapproval = models.StaffExtra.objects.all().filter(user_id=request.user.id, status=True)
        if accountapproval:
            return staffdashboardview(request)
        else:
            return render(request,'qmss/staff_wait_for_approval.html')

#-----------
@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def teacherdashboardview(request):
    return render(request,'qmss/teacherdashboard.html')

@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def teacherapprovedrequestsview(request):
    pen = models.Permission_pdf.objects.filter(user=request.user).filter(status=1)
    context={'pen':pen}
    return render(request,'qmss/teacher_approvedrequests.html',context)

@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def teacherpendingrequestsview(request):
    pen = models.Permission_pdf.objects.filter(user=request.user).filter(status=0)
    context={'pen':pen}
    return render(request,'qmss/teacher_pendingrequests.html',context)

@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def teacherrejectedrequestsview(request):
    pen = models.Permission_pdf.objects.filter(user=request.user).filter(status=2)
    context={'pen':pen}
    return render(request,'qmss/teacher_rejectedrequests.html',context)

@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def teacherrejectrequestview(request,pk):
    pen =models.Permission_pdf.objects.get(id=pk)
    pen.status=2
    pen.save()
    return render(request,'qmss/teacher_pendingrequests.html')

@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def teacherapproverequestview(request,pk):
    pen =models.Permission_pdf.objects.get(id=pk)
    pen.status=1
    pen.save()
    return render(request,'qmss/teacher_pendingrequests.html')




#------------
@login_required(login_url='stafflogin')
@user_passes_test(is_staff)
def staffdashboardview(request):
    return render(request,'qmss/staffdashboard.html')

@login_required(login_url='stafflogin')
@user_passes_test(is_staff)
def staffapprovedrequestsview(request):
    pen = models.Permission_pdf.objects.filter(user=request.user).filter(status=1)
    context={'pen':pen}
    return render(request,'qmss/staff_approvedrequests.html',context)
    

@login_required(login_url='stafflogin')
@user_passes_test(is_staff)
def staffpendingrequestsview(request):
    pen = models.Permission_pdf.objects.filter(user=request.user).filter(status=0)
    context={'pen':pen}
    # print(pen)
    return render(request,'qmss/staff_pendingrequests.html',context)

@login_required(login_url='stafflogin')
@user_passes_test(is_staff)
def staffrejectedrequestsview(request):
    pen = models.Permission_pdf.objects.filter(user=request.user).filter(status=2)
    context={'pen':pen}
    return render(request,'qmss/staff_rejectedrequests.html',context)

@login_required(login_url='stafflogin')
@user_passes_test(is_staff)
def staffrejectrequestview(request,pk):
    pen = models.Permission_pdf.objects.get(id=pk)
    pen.status=2
    pen.save()
    return staffpendingrequestsview(request)

@login_required(login_url='stafflogin')
@user_passes_test(is_staff)
def staffapproverequestview(request,pk):
    pen = models.Permission_pdf.objects.get(id=pk)
    pen.status=1
    pen.save()
    return staffpendingrequestsview(request)

    

# -----------
@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def studentdashboardview(request):
    return render(request,'qmss/studentdashboard.html')

# ---------
@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admindashboardview(request):
    return render(request,'qmss/admindashboard.html')

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def adminstudentview(request):
    return render(request,'qmss/adminstudentview.html')


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_createStudentview(request):
    if request.method == 'POST':
        form1 = forms.StudentUserForm(request.POST)
        form2 = forms.StudentExtraform(request.POST)
        if form1.is_valid() and form2.is_valid():
            user = form1.save()
            user.set_password(user.password)
            user.save()

            f2 = form2.save(commit=False)
            f2.user = user
            f2.status = True
            f2.save()

            my_student_group = Group.objects.get_or_create(name='STUDENT')
            my_student_group[0].user_set.add(user)
            return HttpResponseRedirect('/adminstudentview')
    else:
        form1 = forms.StudentUserForm()
        form2 = forms.StudentExtraform()

    context = {'form1': form1, 'form2': form2}
    return render(request, 'qmss/admin_createStudent.html', context)

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_totalStudentsview(request):
    students = models.StudentExtra.objects.all().filter(status=True)
    student_count = len(students)  
    context = {'students':students,  'student_count':student_count}
    return render(request,'qmss/admin_totalstudents.html',context)

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_updateStudentview(request,pk):
    student = models.StudentExtra.objects.get(id=pk)
    user = models.User.objects.get(id=student.user_id)
    if request.method == 'POST':
        form1 = forms.StudentUserForm(request.POST, instance=user)
        form2 = forms.StudentExtraform(request.POST, instance=student)
        if form1.is_valid() and form2.is_valid():
            user = form1.save()
            user.set_password(user.password)
            user.save()
            f2 = form2.save(commit=False)
            f2.status = True
            f2.save()
            return HttpResponseRedirect('/totalStudents')
    else:
         form1 = forms.StudentUserForm(instance=user)
         form2 = forms.StudentExtraform(instance=student)
         id2 = pk
    context= {'id2':id2,'form1': form1, 'form2': form2}

    return render(request, 'qmss/admin_updateStudent.html', context)

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_deleteStudentview(request,pk):
    student = models.StudentExtra.objects.get(id=pk)
    user = models.User.objects.get(id=student.user_id)
    user.delete()
    student.delete()
    return HttpResponseRedirect('/totalStudents')

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_waitingStudentsview(request):
    students = models.StudentExtra.objects.all().filter(status=False)
    context={'students':students}
    return render(request,'qmss/admin_waitingStudents.html',context)

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_approveStudentview(request,pk):
    student = models.StudentExtra.objects.get (id=pk)
    student.status = True
    student.save ()
    return admin_waitingStudentsview(request)

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_rejectStudentview(request,pk):
    student = models.StudentExtra.objects.get (id=pk)
    user = models.User.objects.get(id=student.user_id)
    user.delete()
    student.delete()
    return admin_waitingStudentsview(request)

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def adminteacherview(request):
    return render(request,'qmss/adminteacherview.html')

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_createTeacherview(request):
    if request.method == 'POST':
        form1 = forms.TeacherUserForm(request.POST)
        form2 = forms.TeacherExtraform(request.POST)
        if form1.is_valid() and form2.is_valid():
            user = form1.save()
            user.set_password(user.password)
            user.save()

            f2 = form2.save(commit=False)
            f2.user = user
            f2.status = True
            f2.save()

            my_teacher_group = Group.objects.get_or_create(name='TEACHER')
            my_teacher_group[0].user_set.add(user)
            return HttpResponseRedirect('/adminteacherview')
    else:
        form1 = forms.TeacherUserForm()
        form2 = forms.TeacherExtraform()

    context = {'form1': form1, 'form2': form2}
    return render(request, 'qmss/admin_createTeacher.html', context)

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_totalTeachersview(request):
    teachers = models.TeacherExtra.objects.all().filter(status=True)
    teacher_count = len(teachers)  
    context = {'teachers':teachers,  'teacher_count':teacher_count}
    return render(request,'qmss/admin_totalTeachers.html',context)

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_updateTeacherview(request,pk):
    teacher = models.TeacherExtra.objects.get(id=pk)
    user = models.User.objects.get(id=teacher.user_id)
    if request.method == 'POST':
        form1 = forms.TeacherUserForm(request.POST, instance=user)
        form2 = forms.TeacherExtraform(request.POST, instance=teacher)
        if form1.is_valid() and form2.is_valid():
            user = form1.save()
            user.set_password(user.password)
            user.save()
            f2 = form2.save(commit=False)
            f2.status = True
            f2.save()
            return HttpResponseRedirect('/totalTeachers')
    else:
        form1 = forms.TeacherUserForm(instance=user)
        form2 = forms.TeacherExtraform(instance=teacher)
        id2 = pk
    context= {'id2':id2,'form1': form1, 'form2': form2}

    return render(request, 'qmss/admin_updateTeacher.html', context)

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_deleteTeacherview(request,pk):
    teacher = models.TeacherExtra.objects.get(id=pk)
    user = models.User.objects.get(id=teacher.user_id)
    user.delete()
    teacher.delete()
    return HttpResponseRedirect('/totalTeachers')

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_waitingTeachersview(request):
    teachers = models.TeacherExtra.objects.all().filter(status=False)
    context={'teachers':teachers}
    return render(request,'qmss/admin_waitingTeachers.html',context)

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_approveTeacherview(request,pk):
    teacher = models.TeacherExtra.objects.get (id=pk)
    teacher.status = True
    teacher.save ()
    return admin_waitingTeachersview(request)

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_rejectTeacherview(request,pk):
    teacher = models.TeacherExtra.objects.get (id=pk)
    user = models.User.objects.get(id=teacher.user_id)
    user.delete()
    teacher.delete()
    return admin_waitingTeachersview(request)


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def adminstaffview(request):
    return render(request,'qmss/adminstaffview.html')


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_createStaffview(request):
    if request.method == 'POST':
        form1 = forms.StaffUserForm(request.POST)
        form2 = forms.StaffExtraform(request.POST)
        if form1.is_valid() and form2.is_valid():
            user = form1.save()
            user.set_password(user.password)
            user.save()

            f2 = form2.save(commit=False)
            f2.user = user
            f2.status = True
            f2.save()

            my_staff_group = Group.objects.get_or_create(name='STAFF')
            my_staff_group[0].user_set.add(user)
            return HttpResponseRedirect('/adminstaffview')
    else:
         form1 = forms.StaffUserForm()
         form2 = forms.StaffExtraform() 
    # print(form1)
    context = {'form1': form1, 'form2': form2}
    return render(request, 'qmss/admin_createStaff.html', context)

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_totalStaffview(request):
    staff = models.StaffExtra.objects.all().filter(status=True)
    staff_count = len(staff)  
    context = {'staff':staff,  'staff_count':staff_count}
    return render(request,'qmss/admin_totalStaff.html',context)

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_updateStaffview(request,pk):
    staff = models.StaffExtra.objects.get(id=pk)
    user = models.User.objects.get(id=staff.user_id)
    if request.method == 'POST':
        
        form1 = forms.StaffUserForm(request.POST, instance=user)
        form2 = forms.StaffExtraform(request.POST, instance=staff)
        if form1.is_valid() and form2.is_valid():
            user = form1.save()
            user.set_password(user.password)
            user.save()
            f2 = form2.save(commit=False)
            f2.status = True
            f2.save()
            return HttpResponseRedirect('/totalStaff')
    else:
        form1 = forms.StaffUserForm(instance=user)
        form2 = forms.StaffExtraform(instance=staff)
        id2 = pk
    context= {'id2':id2,'form1': form1, 'form2': form2}
    return render(request, 'qmss/admin_updateStaff.html', context)

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_deleteStaffview(request,pk):
    staff = models.StaffExtra.objects.get(id=pk)
    user = models.User.objects.get(id=staff.user_id)
    user.delete()
    staff.delete()
    return HttpResponseRedirect('/totalStaff')

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_waitingStaffview(request):
    staff = models.StaffExtra.objects.all().filter(status=False)
    context={'staff':staff}
    return render(request,'qmss/admin_waitingStaff.html',context)

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_approveStaffview(request,pk):
    staff = models.StaffExtra.objects.get (id=pk)
    staff.status = True
    staff.save()
    return admin_waitingStaffview(request)

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_rejectStaffview(request,pk):
    staff = models.StaffExtra.objects.get (id=pk)
    user = models.User.objects.get(id=staff.user_id)
    user.delete()
    staff.delete()
    return admin_waitingStaffview(request)

#----------------
@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def uploadfilesview(request):
    if request.method == 'POST':
        form = forms.PDFFileform(request.POST,request.FILES)
        if form.is_valid():
            pdffile = form.save(sender=request.user)
            return HttpResponseRedirect('postrequests')
    else:
        form = forms.PDFFileform()
    context={'form':form}
    return render(request,'qmss/uploadfiles.html',context)

@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def myuploads(request):
    sendguy = request.user
    uploads = models.PDFFile.objects.filter(sender = sendguy)
    context ={'uploads':uploads}
    # print(uploads)
    return render(request,'qmss/myuploads.html',context)

@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def add_permitted_users(request,pk):
    id2=pk
    shared = models.PDFFile.objects.get(id=pk)
    form = forms.permissions_form()
    linker = models.Permission_pdf()
    # print(form)
    if request.method == 'POST':
        form = forms.permissions_form(request.POST)
        # form= forms.Permission_pdf(request.POST)
        if form.is_valid():
            checker= form.cleaned_data['email']
            taggedguy = models.User.objects.filter(email=checker)
            if len(taggedguy)==1 and not is_admin(taggedguy[0]):
                linker.user= taggedguy[0]
                linker.shared_object=shared
                linker.save()
            else:
                return render(request,'qmss/errormsg.html')
        return HttpResponseRedirect('/myuploads')
    else:
        form = forms.permissions_form()

    context = {'form': form,'id2':id2}
    # print(form)
    return render(request, 'qmss/taguser.html', context)

@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def postrequestsview(request):
    return render(request,'qmss/postrequests.html')

@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def myrequestsview(request):
    return render(request,'qmss/myrequests.html')

@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def student_pendingrequestsview(request):
    myreq = models.PDFFile.objects.filter(sender=request.user)
    queryset1= models.Permission_pdf.objects.filter(user=request.user)
    # queryset2= models.Permission_pdf.objects.filter(user=request.user)
    for req in myreq:
        queryset1 = queryset1 | models.Permission_pdf.objects.filter(shared_object=req)
    queryset1 = queryset1.filter(status=0)
    # for object in queryset1:
    #     queryset2 = queryset2 | models.PDFFile.objects.filter(id=object.shared_object.id)
    
    context = {'pen':queryset1}
    return render(request,'qmss/student_pendingrequests.html',context)

@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def student_approvedrequestsview(request):
    myreq = models.PDFFile.objects.filter(sender=request.user)
    queryset1= models.Permission_pdf.objects.filter(user=request.user)
    # queryset2= models.Permission_pdf.objects.filter(user=request.user)
    for req in myreq:
        queryset1 = queryset1 | models.Permission_pdf.objects.filter(shared_object=req)
    queryset1 = queryset1.filter(status=1)
    # for object in queryset1:
    #     queryset2 = queryset2 | models.PDFFile.objects.filter(pdf_file=object.shared_object)
    
    context = {'pen':queryset1}
    return render(request,'qmss/student_approvedrequests.html',context)

    
@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def student_rejectedrequestsview(request):
    myreq = models.PDFFile.objects.filter(sender=request.user)
    queryset1= models.Permission_pdf.objects.filter(user=request.user)
    # queryset2= models.Permission_pdf.objects.filter(user=request.user)
    for req in myreq:
        queryset1 = queryset1 | models.Permission_pdf.objects.filter(shared_object=req)
    queryset1 = queryset1.filter(status=2)
    # for object in queryset1:
    #     queryset2 = queryset2 | models.PDFFile.objects.filter(pdf_file=object.shared_object)
    
    context = {'pen':queryset1}
    return render(request,'qmss/student_rejectedrequests.html',context)

#------------
def pdf_view(request, year, month, day, filename):
    pdf_file_path = os.path.join(settings.MEDIA_ROOT, 'pdf_files', str(year), str(month), str(day), filename)
    pdf_url = request.build_absolute_uri(pdf_file_path)
    return render(request, 'pdf_view.html', {'url': pdf_url})











