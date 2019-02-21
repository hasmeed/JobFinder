from django.urls import path
from django.views.generic import TemplateView
from .views import (SeekerProfileView,
                    ProviderProfileView,
                    loginView, 
                    logout, 
                    SignUp, 
                    NewCompany,
                    CompanyDetailView,
                    NewJob,JobDetailView, 
                    CompanyListView,
                    UpdateCompany,
                    CompanyJobList,
                    UpdateJob,
                    DeleteCompany,
                    DeleteJob,
                    JobListView,
                    # NewResumee,
                    ResummeCreateView,
                    ResumeeDetail,
                    NewApplication,
                    JobCandidate,
                    ResumeeUpdateView
                    )

from django.contrib.auth import views as auth_views



app_name = 'JobFinderWeb'

urlpatterns = [
    path('', TemplateView.as_view(template_name='JobFinderWeb/home.html'), name='home'),
    path('about/', TemplateView.as_view(template_name='JobFinderWeb/about.html'), name='about'),
    path('contact/', TemplateView.as_view(template_name='JobFinderWeb/contact.html'), name='contact'),
    path('faq/', TemplateView.as_view(template_name='JobFinderWeb/faq.html'), name='faq'),
    path('register/', SignUp, name='register'),
    # path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    # path('login/', auth_views.LoginView.as_view(template_name='JobFinderWeb/login.html'), name='login'),
    path('login/', loginView.as_view(), name='login'),
    path('logout/', logout, name='logout'),
    path('passwordreset/', TemplateView.as_view(template_name='JobFinderWeb/forgotpassword.html'), name='forgotpassword'),
    path('seeker/<str:username>/', SeekerProfileView.as_view(), name='jobseekerprofile'),
    path('provider/addcompany/', NewCompany.as_view(), name='newcompany'),
    path('<slug>/updatecompany/', UpdateCompany.as_view(), name='updatecompany'),
    path('<slug>/deletecompany/', DeleteCompany, name='deletecompany'),
    path('<slug>/deletejob/', DeleteJob, name='deletejob'),
    path('<slug>/updatejob/', UpdateJob.as_view(), name='updatejob'),
    path('<username>/jobs/', CompanyJobList.as_view(), name='companyjobs'),
    path('provider/addjob/', NewJob.as_view(), name='newjob'),
    path('provider/<str:username>/', ProviderProfileView.as_view(), name='jobproviderprofile'),
    path('company/<slug>/', CompanyDetailView.as_view(), name='companydetail'),


    path('companies/', CompanyListView.as_view(), name='companylist'),
    path('companies/<slug>/', CompanyListView.as_view(), name='companylist'),
    # path('companies/<slug>/<location>/', CompanyListView.as_view(), name='companylist'),
    # path('companies/<slug>/<location>/<kword>/', CompanyListView.as_view(), name='companylist'),
    path('joblisting/<slug>/', JobListView.as_view(), name='joblist'),
    path('job/<slug>/', JobDetailView.as_view(), name='jobdetail'),


    # job seeker urls section
    path('newresumee/', ResummeCreateView.as_view(), name='newresumee'),
    path('resumee/<slug>/', ResumeeDetail.as_view(), name='resumeedetail'),
    path('updateresumee/<slug>/', ResumeeUpdateView.as_view(), name='resumeupdate'),
    path('job/application/<jobslug>', NewApplication.as_view(), name='newapplication'),
    path('job/applicant/<jobslug>', JobCandidate.as_view(), name='applicants'),
    
]



