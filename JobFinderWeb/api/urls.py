from django.urls import path
from rest_framework.generics import CreateAPIView
from .views import (JobApi,
                    JobListApi,
                    CompanyApi,
                    CompanyListApi,
                    CompanyJobsApi,
                    CreateCompanyApi,
                    NewJobApi,
                    GetResumeeListApi,
                    SeekerListApi,
                    SeekerDetailApi,
                    GetSeekerResumeeListApi,
                    ResumeeDetailApi,
                    CreateResumeeApi,
                    ApplicantListApi,
                    NewApplicationApi
                    )
from JobFinderWeb.models import Job
from rest_framework_jwt.views import obtain_jwt_token
from rest_framework_swagger.views import get_swagger_view
from rest_framework.documentation import include_docs_urls

schema_view = get_swagger_view(title='JobFinder Api')

app_name = 'JobApi'
urlpatterns = [
    # path('jobs', JobListApi.as_view(), name='joblist'),
    path('login', obtain_jwt_token, name='api-login'),
    path('job/<slug>', JobApi.as_view(), name='jobdetail'),
    path('jobs/', JobListApi.as_view(), name='listjob'),
    path('company/<slug>', CompanyApi.as_view(), name='companyDetail'),
    path('companies/', CompanyListApi.as_view(), name='companyList'),
    path('<slug>/jobs/', CompanyJobsApi.as_view(), name='companyJobList'),
    path('newcompany/', CreateCompanyApi.as_view(), name='newcompany'),
    path('newjob/', NewJobApi.as_view(), name='newjob'),
    path('resumee/', GetResumeeListApi, name='resumeeList'),
    path('resumee/<slug>', ResumeeDetailApi.as_view(), name='resumeeDetail'),
    path('<seeker>/resumee/', GetSeekerResumeeListApi.as_view(),
         name='seekerResumeeList'),
    path('seeker/', SeekerListApi.as_view(), name='seeker'),

    path('newresumee/', CreateResumeeApi.as_view(), name='newresumee'),
    path('seeker/<pk>', SeekerDetailApi.as_view(), name='seekerdetail'),
    path('newapplication/', NewApplicationApi.as_view(), name='newapplication'),
    path('<companyslug>/applicant/', ApplicantListApi.as_view(), name='applicant'),
    path('swagger-docs/', schema_view),
    path('docs/', include_docs_urls(title='JobFinder Api')),
]
