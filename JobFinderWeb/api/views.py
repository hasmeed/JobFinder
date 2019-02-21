from rest_framework import generics, mixins
from JobFinderWeb.models import Job, Provider, Resumee, Seeker, Application
from .serializers import JobSerializer, CompanySerializer, ResumeeSerializer, SeekerSerializer, ApplicationSerializer, NewApplicationSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from JobFinderWeb.models import Company
from rest_framework.mixins import CreateModelMixin
from django.shortcuts import get_object_or_404

from rest_framework.response import Response

from rest_framework import status

from .permissions import IsOwnerOrReadOnly, IsProviderOrReadOnly, IsSeekerOrReadOnly

from django.db.models import Q
from rest_framework.decorators import api_view


class JobApi(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'slug'
    serializer_class = JobSerializer
    permission_classes = [IsOwnerOrReadOnly]

    queryset = Job.objects.all()

    def get_serializer_context(self):
        return {"request": self.request, }


# This allows us to list, search and create
class JobListApi(mixins.CreateModelMixin, generics.ListAPIView):
    lookup_field = 'pk'
    serializer_class = JobSerializer

    def get_queryset(self):
        qs = Job.objects.all()
        query = self.request.GET.get("q")
        if query is not None:
            qs = qs.filter(
                Q(jobtitle__icontains=query) |
                Q(shortdescription__icontains=query)
            ).distinct()
        return qs

    def get_serializer_context(self):
        return {"request": self.request}


class NewJobApi(generics.CreateAPIView, generics.ListAPIView):
    lookup_field = 'pk'
    serializer_class = JobSerializer
    permission_classes = [IsProviderOrReadOnly, ]

    def get_queryset(self):
        return Job.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class CompanyApi(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'slug'
    serializer_class = CompanySerializer
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Company.objects.all()


class CompanyListApi(generics.ListAPIView):  # List of companies
    lookup_field = 'slug'
    serializer_class = CompanySerializer
    # permission_classes = [IsProviderOrReadOnly,]
    queryset = Company.objects.all()

    # def perform_create(self, serializer):
    #     provider  = get_object_or_404(Provider, identity = self.request.user)
    #     serializer.save(user = self.request.user, provider = provider)

    # def post(self, request, *args, **kwargs):
    #     return self.create(request, *args, **kwargs)


class CompanyJobsApi(generics.ListAPIView):  # Company job lists
    lookup_field = 'slug'
    serializer_class = JobSerializer
    # permission_classes = [IsProviderOrReadOnly,]

    def get_queryset(self):
        qs = Job.objects.all()
        query = self.kwargs.get('slug')
        company = get_object_or_404(Company, slug=query)
        if query is not None:
            qs = qs.filter(Company=company)
        return qs


class CreateCompanyApi(generics.CreateAPIView):
    lookup_field = 'pk'
    serializer_class = CompanySerializer
    permission_classes = [IsProviderOrReadOnly]

    def perform_create(self, serializer):
        provider = get_object_or_404(Provider, identity=self.request.user)
        serializer.save(user=self.request.user, provider=provider)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


@api_view(['GET'])
def GetResumeeListApi(request):
    resumee = Resumee.objects.all()
    serializer = ResumeeSerializer(resumee, many=True)
    return Response(serializer.data)


class GetSeekerResumeeListApi(generics.ListAPIView):
    serializer_class = ResumeeSerializer

    def get_queryset(self, *args, **kwargs):
        query = self.kwargs.get("seeker")
        if query is not None:
            qs = Resumee.objects.filter(owner__username=query)
            return qs


class ResumeeDetailApi(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'slug'
    serializer_class = ResumeeSerializer
    permission_classes = [IsOwnerOrReadOnly, ]
    queryset = Resumee.objects.all()


class CreateResumeeApi(generics.CreateAPIView):
    lookup_field = 'pk'
    serializer_class = ResumeeSerializer
    permission_classes = [IsSeekerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class SeekerListApi(generics.ListAPIView):
    lookup_field = 'pk'
    serializer_class = SeekerSerializer
    queryset = Seeker.objects.all()


class SeekerDetailApi(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'pk'
    serializer_class = SeekerSerializer
    permission_classes = [IsOwnerOrReadOnly, ]
    queryset = Seeker.objects.all()


class ApplicantListApi(generics.ListAPIView):
    lookup_field = 'pk'
    serializer_class = ApplicationSerializer
    permission_classes = [IsProviderOrReadOnly]

    def get_queryset(self, *args, **kwargs):
        qs = Application.objects.all()
        companyslug = self.kwargs.get('companyslug')
        if companyslug is not None:
            qs.filter(company__slug=companyslug)
        return qs


class NewApplicationApi(generics.CreateAPIView):
    lookup_field = 'pk'
    serializer_class = ApplicationSerializer
    permission_classes = [IsSeekerOrReadOnly]

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
