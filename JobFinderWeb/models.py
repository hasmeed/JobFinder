from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from django.db.models.signals import pre_save
from .utils import unique_slug_generator
from rest_framework.reverse import reverse as api_reverse

class Identity(AbstractUser):
    is_provider = models.BooleanField(default=False)
    is_seeker = models.BooleanField(default=False)

class CommonInfo(models.Model):
    IsActive = models.BooleanField(default=True)
    IsDeleted = models.BooleanField(default=False)
    timestamp   = models.DateTimeField(auto_now_add=True) 
    updated     = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class CommonAccountInfo(CommonInfo):
    firstname = models.CharField(max_length=50,null=True, blank=True)
    lastname = models.CharField(max_length=50,null=True, blank=True)
    email = models.CharField(max_length=50,null=True, blank=True)
    address = models.CharField(max_length = 120, null=True, blank=True)
    landline = models.CharField(max_length = 120, null=True, blank=True)
    skype = models.CharField(max_length = 120, null=True, blank=True)
    website = models.CharField(max_length = 120, null=True, blank=True)

    class Meta:
        abstract = True


class Seeker(CommonAccountInfo):
    identity = models.OneToOneField(Identity , on_delete=models.CASCADE)
    salary = models.CharField(max_length = 120, null=True, blank=True)
    location = models.CharField(max_length = 120, null=True, blank=True)
    headline = models.CharField(max_length = 120, null=True, blank=True)
    age = models.CharField(max_length = 120, null=True, blank=True)
    # tags = models.CharField(max_length = 120, null=True, blank=True)


     # social media
    facebook = models.CharField(max_length = 120, null=True, blank=True)
    google = models.CharField(max_length = 120, null=True, blank=True)
    pintrest = models.CharField(max_length = 120, null=True, blank=True)
    twitter = models.CharField(max_length = 120, null=True, blank=True)
    git = models.CharField(max_length = 120, null=True, blank=True)
    instagram = models.CharField(max_length = 120, null=True, blank=True)
    youtube = models.CharField(max_length = 120, null=True, blank=True)
    dribbble = models.CharField(max_length = 120, null=True, blank=True)
    # end of social media 
    
    @property
    def owner(self):
        return self.identity

    def __str__(self):
        return "{} {}".format(self.firstname,self.lastname)

    def get_absolute_url(self):
        return reverse('JobFinderWeb:jobseekerprofile', kwargs={'username':self.identity.username})

    def get_api_uri(self, request=None):
        return api_reverse('JobApi:seekerdetail', kwargs={'pk': self.pk}, request=request) 

    def get_seeker_resumee_uri(self, request=None):
        return api_reverse('JobApi:seekerResumeeList', kwargs={'seeker':self.identity}, request=request)
 

class Provider(CommonAccountInfo):
    identity = models.OneToOneField(Identity , on_delete=models.CASCADE)    

    def get_absolute_url(self):
        return reverse('JobFinderWeb:jobseekerprofile', kwargs={'username':self.identity.username})


    def __str__(self):
        return '{} {}'.format(self.firstname, self.lastname)

    # def __str__(self):
    #         return self.companyname

def upload_location(instance, filename):
    return "{}/{}".format(instance.id, filename)

class Company(CommonInfo):
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE)
    companyname = models.CharField(max_length = 120, null=True, blank=True)
    headline = models.CharField(max_length = 120, null=True, blank=True)
    shortdescription = models.TextField(null=True, blank=True)
    location = models.CharField(max_length = 120, null=True, blank=True)
    founded = models.CharField(max_length = 120,null=True, blank=True)
    no_of_employees = models.CharField(max_length = 120, null=True, blank=True)
    companydetails = models.TextField(null=True, blank=True)
    slug = models.SlugField(null = True, blank = True)
    category = models.CharField(max_length = 120, null = True, blank = True)
    logo = models.ImageField(upload_to = 'company', null=True, blank=True, height_field='height_field', width_field='width_field')
    height_field = models.IntegerField(default=0, null=True, blank=True)
    width_field = models.IntegerField(default=0, null=True, blank=True)
    coverimage = models.ImageField(null=True, upload_to='coverimge', blank=True, height_field='height_field', width_field='width_field')

    email = models.CharField(max_length=50,null=True, blank=True)
    phonenumber = models.CharField(max_length = 120,null=True, blank=True)
    website = models.CharField(max_length = 120, null=True, blank=True)

     # social media
    facebook = models.CharField(max_length = 120, null=True, blank=True)
    google = models.CharField(max_length = 120, null=True, blank=True)
    pinterest = models.CharField(max_length = 120, null=True, blank=True)
    twitter = models.CharField(max_length = 120, null=True, blank=True)
    git = models.CharField(max_length = 120, null=True, blank=True)
    instagram = models.CharField(max_length = 120, null=True, blank=True)
    youtube = models.CharField(max_length = 120, null=True, blank=True)
    dribbble = models.CharField(max_length = 120, null=True, blank=True)
    # end of social media 
    user = models.ForeignKey(Identity, on_delete=models.CASCADE, null = True, blank = True)

    def remove(self):
        self.IsActive = False


    @property
    def title(self):
        return self.companyname

    @property
    def owner(self):
        return self.user

    def __str__(self):
            return self.companyname

    def countjob(self):
        return Job.objects.filter(Company__companyname = self.companyname, IsActive = True).count()

    class Meta:
        ordering = ['-updated','-timestamp']

    def get_absolute_url(self):
        return reverse('JobFinderWeb:companydetail', kwargs={'slug':self.slug})

    def get_api_uri(self, request=None):
        return api_reverse('JobApi:companyDetail', kwargs={'slug': self.slug}, request=request) 

    def get_job_list_uri(self, request=None):
        return api_reverse('JobApi:companyJobList', kwargs={'slug': self.slug}, request=request) 

    def itsowner(self, user):
        return user == self.user 


def company_pre_save_reciever(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


pre_save.connect(company_pre_save_reciever, sender=Company)



class Job(CommonInfo):
    jobtitle = models.CharField(max_length = 120, null=True, blank=True)
    Company = models.ForeignKey(Company, on_delete=models.CASCADE)
    shortdescription = models.TextField(null=True, blank=True)
    applicationurl = models.TextField(null=True, blank=True)
    location = models.CharField(max_length = 120, null=True, blank=True)
    workinghour = models.CharField(max_length = 120, null=True, blank=True)
    yearsofexperience = models.CharField(max_length = 120, null=True, blank=True)
    salary = models.CharField(max_length = 120, null=True, blank=True)
    degree = models.CharField(max_length = 120, null=True, blank=True)
    timetype = models.CharField(max_length = 120, null=True, blank=True) # partime, full time 
    description = models.TextField(null=True, blank=True)
    jobstatus = models.CharField(max_length=50, null=True, blank=True)
    category = models.CharField(max_length = 120, null = True, blank = True)
    slug = models.SlugField(null = True, blank = True)
    user = models.ForeignKey(Identity, on_delete=models.CASCADE)
    height_field = models.IntegerField(default=0, null=True, blank=True)
    width_field = models.IntegerField(default=0, null=True, blank=True)
    coverimage = models.ImageField(null=True, upload_to='jobcoverimge', blank=True, height_field='height_field', width_field='width_field')

    @property
    def owner(self):
        return self.user

    def __str__(self):
        return self.jobtitle

    @property
    def title(self):
        return self.jobtitle

    def get_absolute_url(self):
        return reverse('JobFinderWeb:jobdetail', kwargs={"slug": self.slug})

    # This is for api. and it will show the domain name with the url. e.g. 'localhost:8000/api/jobs/2' while the reverse wont show the localhost part
    def get_api_url(self, request=None):
        return api_reverse('JobApi:jobdetail', kwargs={'slug': self.slug}, request=request) 

     
    def itsowner(self, user):
        return user == self.user 


def job_pre_save_reciever(sender, instance, *args, **kwargs):
    if not instance.slug: 
        instance.slug = unique_slug_generator(instance)


pre_save.connect(job_pre_save_reciever, sender=Job)


class Resumee(CommonInfo):
    name = models.CharField(max_length = 120, null=True, blank=True)
    headline = models.CharField(max_length = 120, null=True, blank=True)
    shortdescription = models.CharField(max_length = 120, null=True, blank=True)
    salary = models.CharField(max_length = 120, null=True, blank=True)
    location = models.CharField(max_length = 120, null=True, blank=True)
    headline = models.CharField(max_length = 120, null=True, blank=True)
    age = models.CharField(max_length = 120, null=True, blank=True)
    tags = models.CharField(max_length = 120, null=True, blank=True)
    mobile = models.CharField(max_length = 120, null=True, blank=True)
    email = models.CharField(max_length = 120, null=True, blank=True)
    status = models.CharField(max_length = 120, null=True, blank=True)
    website = models.CharField(max_length = 120, null=True, blank=True)
    slug = models.SlugField(null = True, blank = True)


     # social media
    facebook = models.CharField(max_length = 120, null=True, blank=True)
    google = models.CharField(max_length = 120, null=True, blank=True)
    pintrest = models.CharField(max_length = 120, null=True, blank=True)
    twitter = models.CharField(max_length = 120, null=True, blank=True)
    git = models.CharField(max_length = 120, null=True, blank=True)
    instagram = models.CharField(max_length = 120, null=True, blank=True)
    youtube = models.CharField(max_length = 120, null=True, blank=True)
    dribbble = models.CharField(max_length = 120, null=True, blank=True)
    # end of social media 
    owner = models.ForeignKey(Identity, on_delete=models.CASCADE)


    def __str__(self):
        return "{}".format(self.name)

    @property
    def title(self):
        return self.name

    def get_absolute_url(self):
        return reverse('JobFinderWeb:resumeedetail', kwargs={"slug": self.slug})

    def get_api_url(self, request=None):
        return api_reverse('JobApi:resumeeDetail', kwargs={'slug': self.slug}, request=request) 


def resumee_pre_save_reciever(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


pre_save.connect(resumee_pre_save_reciever, sender=Resumee)


class Education(CommonInfo):
    # education 
    degree = models.CharField(max_length = 120, null=True, blank=True)
    major = models.CharField(max_length = 120, null=True, blank=True)
    school = models.CharField(max_length = 120, null=True, blank=True)
    datefrom = models.CharField(max_length = 120, null=True, blank=True)
    dateto = models.CharField(max_length = 120, null=True, blank=True)
    shortdescription = models.CharField(max_length = 120, null=True, blank=True)
    owner = models.ForeignKey(Identity, on_delete=models.CASCADE, null=True, blank=True)
    resumee = models.ForeignKey(Resumee, on_delete=models.CASCADE, null=True, blank=True)


class Skill(CommonInfo): 
    # education 
    skillname = models.CharField(max_length = 120, null=True, blank=True)
    proficiency = models.CharField(max_length = 120, null=True, blank=True)
    owner = models.ForeignKey(Identity, on_delete=models.CASCADE, null=True, blank=True)
    resumee = models.ForeignKey(Resumee, on_delete=models.CASCADE, null=True, blank=True)



class Experience(CommonInfo):
    # experience 
    companyname = models.CharField(max_length = 120, null=True, blank=True)
    position = models.CharField(max_length = 120, null=True, blank=True)
    datefrom = models.CharField(max_length = 120, null=True, blank=True)
    dateto = models.CharField(max_length = 120, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    owner = models.ForeignKey(Identity, on_delete=models.CASCADE, null=True, blank=True)
    resumee = models.ForeignKey(Resumee, on_delete=models.CASCADE, null=True, blank=True)
    # end of experience 

class Application(CommonInfo):
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    resumee = models.ForeignKey(Resumee, on_delete=models.CASCADE, null=True, blank=True)
    candidate = models.ForeignKey(Seeker, on_delete=models.CASCADE, null=True, blank=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True)
    applicationstatus = models.CharField(max_length = 120, null=True, blank=True, default="New")

    def get_resume_api(self, request = None):
        return api_reverse('JobApi:resumeeDetail', kwargs={'slug': self.resumee.slug}, request=request)

    def get_candidate_api(self, request = None):
        return api_reverse('JobApi:seekerdetail', kwargs={'pk': self.candidate.pk}, request=request)

    def get_job_api(self, request = None):
        return api_reverse('JobApi:jobdetail', kwargs={'slug': self.job.slug}, request=request)

    def get_company_api(self, request = None):
        return api_reverse('JobApi:companyDetail', kwargs={'slug': self.company.slug}, request=request)

    def __str__(self):
        return self.job.jobtitle



class CustomJobApplication(CommonInfo):
    application = models.ForeignKey(Application, on_delete=models.CASCADE)
    name = models.CharField(max_length = 120, null=True, blank=True)
    email = models.CharField(max_length = 120, null=True, blank=True)
    message = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

    
