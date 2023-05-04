"""Defines Url patterns for QMSS"""

from django.urls import path
from . import views
from django.contrib.auth.views import LoginView,LogoutView
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static



# from django.conf import settings
# from django.conf.urls.static import static

app_name = 'qmss'
urlpatterns = [
    #Home page
    path('',views.index,name='index'),
    path('base',views.base,name='base'),
    path('adminclick', views.adminclick_view, name='adminclick'),
    path('teacherclick', views.teacherclick_view,name='teacherclick'),
    path('studentclick', views.studentclick_view,name='studentclick'),
    path('staffclick', views.staffclick_view,name='staffclick'),



    path('adminsignup', views.admin_signup_view,name='adminsignup'),
    path('studentsignup', views.student_signup_view,name='studentsignup'),
    path('teachersignup', views.teacher_signup_view),
    path('staffsignup', views.staff_signup_view),


    path('adminlogin', LoginView.as_view(template_name='qmss/adminlogin.html')),
    path('studentlogin', LoginView.as_view(template_name='qmss/studentlogin.html')),
    path('teacherlogin', LoginView.as_view(template_name='qmss/teacherlogin.html')),
    path('stafflogin',LoginView.as_view(template_name='qmss/stafflogin.html')),


    path('afterlogin', views.afterlogin_view,name='afterlogin'),

    path('logout', LogoutView.as_view(template_name='qmss/index.html'), name='logout'),

    path('admindashboard', views.admindashboardview,name='admindashboard'),
    path('adminstudentview',views.adminstudentview,name='adminstudentview'),
    path('totalStudents',views.admin_totalStudentsview,name='totalStudents'),
    path('updateStudent/<int:pk>/',views.admin_updateStudentview,name='admin_studentUpdateview'),
    path('deleteStudent/<int:pk>/',views.admin_deleteStudentview),
    path('waitingStudents',views.admin_waitingStudentsview,name='waitingStudentsview'),
    path('approveStudent/<str:pk>/',views.admin_approveStudentview,name='approvestudent'),
    path('rejectStudent/<int:pk>/',views.admin_rejectStudentview,name='rejectstudent'),
    path('createStudent',views.admin_createStudentview,name='createStudent'),

    path('adminteacherview',views.adminteacherview,name='adminteacherview'),
    path('totalTeachers',views.admin_totalTeachersview,name='totalTeachers'),
    path('updateTeacher/<int:pk>/',views.admin_updateTeacherview,name='admin_teacherUpdateview'),
    path('deleteTeacher/<int:pk>/',views.admin_deleteTeacherview),
    path('waitingTeachers',views.admin_waitingTeachersview,name='waitingTeachersview'),
    path('approveTeacher/<str:pk>/',views.admin_approveTeacherview,name='approveteacher'),
    path('rejectTeacher/<int:pk>/',views.admin_rejectTeacherview,name='rejectTeacher'),
    path('createTeacher',views.admin_createTeacherview,name='createTeacher'),

    path('adminstaffview',views.adminstaffview,name='adminstaffview'),
    path('totalStaff',views.admin_totalStaffview,name='totalStaff'),
    path('updateStaff/<int:pk>/',views.admin_updateStaffview,name='admin_staffUpdateview'),
    path('deleteStaff/<int:pk>/',views.admin_deleteStaffview),
    path('waitingStaff',views.admin_waitingStaffview,name='waitingStaffview'),
    path('approveStaff/<str:pk>/',views.admin_approveStaffview,name='approvestaff'),
    path('rejectStaff/<int:pk>/',views.admin_rejectStaffview,name='rejectStaff'),
    path('createStaff',views.admin_createStaffview,name='createStaff'),

    path('studentdashboard',views.studentdashboardview,name='studentdashboard'),
    path('teacherdashboard',views.teacherdashboardview,name='teacherdashboard'),
    path('teacherdashboard',views.staffdashboardview,name='teacherdashboard'),
    path('staffapprovedrequests',views.staffapprovedrequestsview,name='staff_apro_req'),
    path('staffrejectedrequests',views.staffrejectedrequestsview,name='staff_rej_req'),
    path('staffpendingrequests',views.staffpendingrequestsview,name='staff_pen_req'),
    path('staffapproverequest',views.staffapproverequestview),
    path('staffrejectrequest',views.staffrejectrequestview),
    path('teacherapprovedrequests',views.teacherapprovedrequestsview,name='teacher_pro_req'),
    path('teacherpendingrequests',views.teacherpendingrequestsview,name='teachers_pen_req'),
    path('teacherrejectedrequests',views.teacherrejectedrequestsview,name='teachers_rej_req'),
    path('teacherapproverequest',views.teacherapproverequestview),
    path('teacherrejectrequest',views.teacherrejectrequestview),
    path('myrequests',views.myrequestsview,name='myrequests'),
    path('postrequests',views.postrequestsview,name='postrequests'),
    path('myuploads',views.myuploads,name='myuploads'),
    path('uploadpdf',views.uploadfilesview,name='uploadpdf'),
    path('taguser/<int:pk>/',views.add_permitted_users),
    path('studentapprovedrequests',views.student_approvedrequestsview),
    path('studentpendingrequests',views.student_pendingrequestsview),
    path('studentrejectedrequests',views.student_rejectedrequestsview),
    path('staffapproverequest/<int:pk>/',views.staffapproverequestview),
    path('staffrejectrequest/<int:pk>/',views.staffrejectrequestview),
    path('teacherapproverequest/<int:pk>/',views.teacherapproverequestview),
    path('teacherrejectrequest/<int:pk>/',views.teacherrejectrequestview),
    path('pdf_files/<int:year>/<int:month>/<int:day>/<str:filename>', TemplateView.as_view(template_name='pdf_view.html'), name='pdf_view'),



    
    # path('studentprocessedrequest',views.studentprocessedrequestsview,name='st_pro_req'),
    # path('studentpendingrequests',views.studentpendingrequestsview,name='stu_pen_req'),
 

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
