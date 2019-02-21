from rest_framework import serializers
from JobFinderWeb.models import Job, Company, Resumee, Seeker, Application
from rest_framework.reverse import reverse as api_reverse
from django.shortcuts import get_object_or_404

class ProviderCompanyForeignKey(serializers.PrimaryKeyRelatedField):
    def get_queryset(self):
        return Company.objects.filter(user=self.context['request'].user)

class ResumeeForeignKey(serializers.PrimaryKeyRelatedField):
    def get_queryset(self):
        return Resumee.objects.filter(owner=self.context['request'].user)

class JobSerializer(serializers.ModelSerializer):
    uri = serializers.SerializerMethodField(read_only=True)
    Company = ProviderCompanyForeignKey()
    class Meta:
        model = Job
        fields = [
            'uri',
            # 'pk',
            'jobtitle',
            'Company',
            'location',
            'workinghour',
            'salary',
            'yearsofexperience',
            'degree',
            'timetype',
            'coverimage',
            # 'user',
        ]


    def get_uri(self, obj):
        request = self.context.get("request")
        return obj.get_api_url(request=request)


        # fields = '__all__'
        # this is used to make a field a read only
        # read_only_fields = [
        #     'Company'
        # ]
       
    def validate_jobtitle(self,value):
        qs = Job.objects.filter(jobtitle__iexact = value)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError('job title already exists')
        return value

class ResumeeSerializer(serializers.ModelSerializer):
    uri = serializers.SerializerMethodField(read_only=True)
    # uri = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Resumee
        exclude = ['owner','IsActive', 'IsDeleted']
        # fields = '__all__'
        # read_only_fields = [
        #     'owner'
        # ]

    def get_uri(self, obj):
        request = self.context.get('request')
        return obj.get_api_url(request)

    # def get_owner(self, obj):
    #     request = self.context.get('request')
    #     identity = obj.owner
    #     seeker = get_object_or_404(Seeker, identity = identity)
    #     return seeker.get_api_uri(request = request)

class SeekerSerializer(serializers.ModelSerializer):
    uri = serializers.SerializerMethodField(read_only=True)
    resumees = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Seeker
        exclude = ['identity', 'IsActive', 'IsDeleted']

    def get_uri(self, obj):
        request = self.context.get("request")
        return obj.get_api_uri(request=request)

    def get_resumees(self, obj):
        request = self.context.get("request")
        return obj.get_seeker_resumee_uri(request=request)


class CompanySerializer(serializers.ModelSerializer):
    uri = serializers.SerializerMethodField(read_only=True)
    jobscount = serializers.SerializerMethodField(read_only=True)
    jobs = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Company
        fields = [
            'uri',
            'jobscount',
            'jobs',
            # 'provider',
            'companyname',
            'location',
            'email',
            'phonenumber',
            'website',
        ]
        read_only_fields = [
            # 'provider'
        ]

    def get_jobscount(self, obj):
        return obj.countjob()

    def get_uri(self, obj):
        request = self.context.get('request')
        return obj.get_api_uri(request = request)

    def get_jobs(self, obj):
        request = self.context.get('request')
        return obj.get_job_list_uri(request=request)


class ApplicationSerializer(serializers.ModelSerializer):
    resumeeuri = serializers.SerializerMethodField(read_only=True)
    candidateurl = serializers.SerializerMethodField(read_only=True)
    joburl = serializers.SerializerMethodField(read_only=True)
    companyurl = serializers.SerializerMethodField(read_only=True)
    resumee = ResumeeForeignKey()
    
    class Meta:
        model = Application
        # fields = '__all__'
        exclude = ['IsActive','IsDeleted',]
        read_only_fields = ('candidate', 'company', 'applicationstatus')

    def create(self, validated_data):
        job = validated_data.pop("job")
        resumee = validated_data.pop("resumee")
        company = job.Company
        seeker = get_object_or_404(Seeker, identity = self.context['request'].user)
        application = Application.objects.create(resumee = resumee, job = job, company = company, candidate = seeker)
        
        return application
                

    def get_resumeeuri(self, obj):
        request = self.context.get('request')
        return obj.get_resume_api(request = request)
    
    def get_candidateurl(self, obj):
        request = self.context.get('request')
        return obj.get_candidate_api(request = request)

    def get_joburl(self, obj):
        request = self.context.get('request')
        return obj.get_job_api(request = request)

    def get_companyurl(self, obj):
        request = self.context.get('request')
        return obj.get_company_api(request = request)

        



class NewApplicationSerializer(serializers.ModelSerializer):
    resumee = ResumeeForeignKey()
    class Meta:
        model = Application
        # fields = '__all__'
        exclude = ['IsActive','IsDeleted','candidate', 'company','applicationstatus',]
