from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .forms import SignUpForm,LoginForm, CompanyForm, JobForm, ResumeeForm, CustomApplicationForm
from django.contrib.auth import authenticate, login as s, logout as log_out
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.db.models import Q
from django.contrib import messages
import operator
from django.forms import formset_factory,modelformset_factory

from .models import Seeker,Education,Experience,Skill,Provider,Company,Job,Resumee,Application,Identity,CustomJobApplication

from .decorators import provider_required, jobseeker_required

from django.contrib.auth.hashers import make_password
from django.contrib.auth import login as auth_login

from django.contrib.auth import get_user_model
User = get_user_model() 

from django.conf import settings
from .forms import EducationFormSet,ExperienceFormSet, SkillFormSet


@method_decorator([jobseeker_required], name="dispatch")
class NewApplication(View):
    template_name = 'JobFinderWeb/application.html'
    form_class = CustomApplicationForm
    model = CustomJobApplication

    def get(self, request, *args, **kwargs):
        jobform = self.form_class
        slug = self.kwargs.get('jobslug')
        job = get_object_or_404(Job, slug=slug)
        resumee = Resumee.objects.filter(owner = self.request.user)
        print(resumee)
        context = {
            'job':job,
            'resumees':resumee,
            'jobform':jobform
        }
        return render(request, self.template_name, context)

    
    def post(self, request, *args, **kwargs):
        customform = self.form_class(self.request.POST)
        slug = self.kwargs.get('jobslug')
        job = get_object_or_404(Job, slug=slug)
        resumeeSlug = self.request.POST.get('slug')

        if resumeeSlug:
            resumee = get_object_or_404(Resumee, slug = resumeeSlug)
            Application.objects.create(
                job = job,
                resumee = resumee, 
                candidate = get_object_or_404(Seeker, identity = self.request.user),
                company = job.Company
            )

            messages.success(request, "You have successfully apply for {} with {} resumee".format(job.jobtitle, resumee.name))
            return HttpResponseRedirect('/seeker/{}'.format(self.request.user.username))
        else:
            if customform.is_valid():
                application = Application.objects.create(
                job = job,
                resumee = None,
                candidate = get_object_or_404(Seeker, identity = self.request.user),
                company = job.Company
                )

                CustomJobApplication.objects.create(
                    application = application,
                    name = customform.cleaned_data.get('name'),
                    email = customform.cleaned_data.get('email'),
                    message = customform.cleaned_data.get('message')
                )

                messages.success(request, "You have successfully apply for {} with custom resumee".format(job.jobtitle))
            return HttpResponseRedirect('/seeker/{}'.format(self.request.user.username))

   
class JobCandidate(View):
    template_name = 'JobFinderWeb/applicants.html'

    def get(self, request, *args, **kwargs):
        slug = self.kwargs.get('jobslug')
        job = get_object_or_404(Job, slug=slug)
        resumee = Resumee.objects.filter(owner = self.request.user)
        applicant = Application.objects.filter(job = job)
        context = {
            'job':job,
            'resumees':resumee,
            'applicants':applicant
            
        }
        return render(request, self.template_name, context)


class ResummeCreateView(CreateView):
    template_name = 'JobFinderWeb/newresumee.html'
    model = Resumee
    form_class = ResumeeForm
    success_url = '/'

    def get(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        education_form = EducationFormSet()
        experience_form = ExperienceFormSet()
        skill_form = SkillFormSet()

        return self.render_to_response(self.get_context_data(resumee_form=form, 
                                                            education_form = education_form, 
                                                            experience_form=experience_form,
                                                            skill_form=skill_form,title ="Add new Resumee"))


    def post(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        education_form = EducationFormSet(self.request.POST)
        experience_form = ExperienceFormSet(self.request.POST)
        skill_form = SkillFormSet(self.request.POST)
        if (form.is_valid() and education_form.is_valid() and experience_form.is_valid() and skill_form.is_valid()):
            return self.form_valid(form, education_form, experience_form, skill_form)
        else:
            return self.form_invalid(form, education_form, experience_form, skill_form)

    def form_valid(self, form, education_form, experience_form, skill_form):
        self.object = form.save(commit=False)
        self.object.owner = self.request.user
        self.object.status = "show"
        self.object.save()

        education_form.instance = self.object
        edu = education_form.save(commit=False)
        for ed in edu:
            ed.owner = self.request.user
            ed.IsActive = True
            education_form.save()

        experience_form.instance = self.object
        exp = experience_form.save(commit=False)
        for ex in exp:
            ex.owner = self.request.user
            ex.IsActive = True
            experience_form.save()

        skill_form.instance = self.object
        skills = skill_form.save(commit=False)
        for skill in skills:
            skill.owner = self.request.user
            skill.IsActive = True
            skill_form.save()
        
        return HttpResponseRedirect(self.get_success_url())

    
    def form_invalid(self, form, education_form, experience_form, skill_form):
        return self.render_to_response(self.get_context_data(resumee_form=form, 
                                                            education_form = education_form, 
                                                            experience_form=experience_form,
                                                            skill_form=skill_form))


# from django.core.paginator import Paginator


class JobListView(ListView):
    template_name = 'JobFinderWeb/joblist.html'

    def get_queryset(self, *args, **kwargs):
        slug = self.kwargs.get("slug")
        if slug != 'None':
            try:
                querysetValue = Job.objects.filter(Q(category__iexact = slug) |
                                Q(category__icontains = slug))
            except querysetValue.DoesNotExist:
                raise Http404("Job does not exist")
            queryset = querysetValue
        else:
            queryset = Job.objects.filter(IsActive=True)
        # paginator = Paginator(queryset, 3)
        
        return queryset

    

    def get_context_data(self, *args, **kwargs):
        context = super(JobListView, self).get_context_data(*args, **kwargs)
        context['media_url'] = settings.MEDIA_URL
        if self.kwargs.get("slug") != "None":
            context['category'] = self.kwargs.get("slug")
            # page =  self.request.GET.get('page')
        else:
            context['category'] = "All"
            # page =  self.request.GET.get('page')
        return context


def SignUp(request):
    form = SignUpForm(request.POST or None)
    template_name = 'jobfinderweb/register.html'
    if form.is_valid():
        

        if request.POST.get('accounttype') == 'jobseeker':

            IndentiyDetails = User.objects.create(
            username = request.POST.get('username'), # request.POST.get('username') or request.POST'username'[]
            password = make_password(request.POST.get('password')),
            first_name = form.cleaned_data.get('firstname'),
            last_name = form.cleaned_data.get('lastname'),
            email = form.cleaned_data.get('email'),
            is_seeker = True
            )

            Seeker.objects.create(
                identity = IndentiyDetails,
                firstname = form.cleaned_data.get('firstname'),
                lastname = form.cleaned_data.get('lastname'),
                email = form.cleaned_data.get('email'),
                
                )
            auth_login(request, IndentiyDetails)
            return HttpResponseRedirect('/')

        else:
            IndentiyDetails = User.objects.create(
            username = request.POST.get('username'), # request.POST.get('username') or request.POST'username'[]
            password = make_password(request.POST.get('password')),
            first_name = form.cleaned_data.get('firstname'),
            last_name = form.cleaned_data.get('lastname'),
            email = form.cleaned_data.get('email'),
            is_provider = True
            )

            Provider.objects.create(
                identity = IndentiyDetails,
                firstname = form.cleaned_data.get('firstname'),
                lastname = form.cleaned_data.get('lastname'),
                email = form.cleaned_data.get('email'),
                )
            auth_login(request, IndentiyDetails)
            return HttpResponseRedirect('/')
    
    else:
       return render(request, template_name, {'form': form})


class SeekerProfileView(LoginRequiredMixin,DetailView):
    template_name = 'jobfinderweb/seekprofile.html'
    queryset = Seeker.objects.all() 

    def get_object(self, *args, **kwargs):
        username = self.kwargs.get("username")
        user = User.objects.get(username__iexact = username)
        userinfo = get_object_or_404(Seeker, identity=user)
            
        obj = get_object_or_404(Seeker, id = userinfo.id) # pk = rest_id
        return obj

    def get_context_data(self, *args, **kwargs):
        context = super(SeekerProfileView, self).get_context_data(*args, **kwargs)
        applications = Application.objects.filter(candidate__identity = self.request.user )
        resumee = Resumee.objects.filter(owner = self.request.user)
        context['resumees'] = resumee
        context['applications'] = applications
        return context
    

class ResumeeDetail(DetailView):
    template_name = 'jobfinderweb/resumeedetail.html'
    queryset = Resumee.objects.all()

    def get_object(self, *args, **kwargs):
        slug = self.kwargs.get('slug')
        resumee = get_object_or_404(Resumee, slug=slug)
        return resumee
    
    def get_context_data(self, *args, **kwargs):
        context = super(ResumeeDetail, self).get_context_data(*args,**kwargs)
        resumee = get_object_or_404(Resumee, slug = self.kwargs.get('slug'))
        educations = Education.objects.filter(resumee = resumee)
        experience = Experience.objects.filter(resumee = resumee)
        skills = Skill.objects.filter(resumee = resumee)
        context['educations'] = educations
        context['experience'] = experience
        context['skills'] = skills
        return context


class ProviderProfileView(LoginRequiredMixin,DetailView):
    template_name = 'jobfinderweb/providerprofile.html'
    queryset = Provider.objects.all()

    def get_object(self, *args, **kwargs):
        username = self.kwargs.get("username")
        user = get_object_or_404(User, username__iexact = username)
        userinfo = Provider.objects.get(identity = user)
            
        obj = get_object_or_404(Provider, id = userinfo.id) # pk = rest_id
        return obj
    
    def get_context_data(self, **kwargs):
        context = super(ProviderProfileView, self).get_context_data(**kwargs)
        context['companyinfo'] = Company.objects.filter(provider__identity = self.request.user, IsActive=True)
        context['media_url'] = settings.MEDIA_URL
        return context


class CompanyDetailView(DetailView):
    template_name = 'jobfinderweb/companydetail.html'
    queryset = Company.objects.filter(IsActive = True)

    def get_context_data(self, **kwargs):
        context = super(CompanyDetailView, self).get_context_data(**kwargs)
        company = get_object_or_404(Company, slug = context['company'].slug)
        context['itsowner'] = company.itsowner(self.request.user)
        context['jobs'] = Job.objects.filter(Company = company, IsActive=True)
        context['media_url'] = settings.MEDIA_URL
        return context
    
    
class JobDetailView(DetailView):
    template_name = 'jobfinderweb/jobdetail.html'
    queryset = Job.objects.all()

    def get_context_data(self, *args, **kwargs):
        context = super(JobDetailView, self).get_context_data(*args, **kwargs)
        job = get_object_or_404(Job, slug = context['job'].slug)
        if self.request.user.is_authenticated:
            application = Application.objects.filter(candidate__identity = self.request.user, job= job)
            if application:
                context['alreadyapply'] = True
        context['itsowner'] = job.itsowner(self.request.user)
        context['media_url'] = settings.MEDIA_URL
        return context
    

class loginView(View):
    template_name = 'jobfinderweb/login.html'
    form_class = LoginForm

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                if user.is_provider:
                    auth_login(request, user)
                    context = {}
                    return HttpResponseRedirect('/provider/{}'.format(user.username))
                elif user.is_seeker:
                    auth_login(request, user)
                    context = {}
                    return HttpResponseRedirect('/seeker/{}'.format(user.username))
            else:
                errors = 'invalid username and password'

        context = {'form':form,'errors':errors}
        return render(request, self.template_name, context)


class NewCompany(LoginRequiredMixin,CreateView): 
    form_class = CompanyForm
    template_name = 'JobFinderWeb/newcompany.html'


    def form_valid(self, form):
        instance = form.save(commit=False)
        provider = get_object_or_404(Provider, identity = self.request.user)
        instance.provider = provider
        instance.user = self.request.user
        instance.IsActive = True
        return super(NewCompany, self).form_valid(form)

    def get_context_data(self,*args, **kwargs):
            context = super(NewCompany, self).get_context_data(*args, **kwargs)
            context['title'] = "Create New Company"
            return context


class UpdateCompany(LoginRequiredMixin,UpdateView):
    form_class = CompanyForm
    template_name = 'JobFinderWeb/updatecompany.html'


    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.IsActive = True
        return super(UpdateCompany, self).form_valid(form)


    def get_queryset(self):
        provider = get_object_or_404(Provider, identity = self.request.user)    
        return Company.objects.filter(provider = provider)

    def get_context_data(self,*args, **kwargs):
            context = super(UpdateCompany, self).get_context_data(*args, **kwargs)
            context['title'] = "Update Company"
            return context


class ResumeeUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'JobFinderWeb/updareresumee.html'
    form_class = ResumeeForm

    def get_queryset(self):
        return Resumee.objects.filter(owner = self.request.user)


    def get_context_data(self,*args, **kwargs):
            context = super(ResumeeUpdateView, self).get_context_data(*args, **kwargs)
            context['title'] = "Update Resumee"
            return context


@method_decorator([provider_required], name="dispatch")
class NewJob(LoginRequiredMixin,CreateView):
    form_class = JobForm
    template_name = 'JobFinderWeb/newjob.html'

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.user = self.request.user
        instance.jobstatus = 'Open'
        instance.IsActive = True
        return super(NewJob, self).form_valid(form)

    def get_form_kwargs(self):
        kwargs = super(NewJob, self).get_form_kwargs()
        provider = get_object_or_404(Provider, identity=self.request.user)
        kwargs['user'] = provider
        return kwargs


    def get_context_data(self, **kwargs):
        context = super(NewJob, self).get_context_data(**kwargs)
        return context


class UpdateJob(LoginRequiredMixin,UpdateView):
    form_class = JobForm
    template_name = 'JobFinderWeb/updatejob.html'

    def get_queryset(self):
        return Job.objects.filter(user = self.request.user)    

    def get_form_kwargs(self):
        kwargs = super(UpdateJob, self).get_form_kwargs()
        provider = Provider.objects.get(identity=self.request.user)
        kwargs['user'] = provider
        return kwargs

    def get_context_data(self,*args, **kwargs):
            context = super(UpdateJob, self).get_context_data(*args, **kwargs)
            context['title'] = "Update Job"
            return context

    def form_valid(self, form):
        print('this is all valid----------------')
        instance = form.save(commit=False)
        instance.IsActive = True
        instance.user = self.request.user
        return super(UpdateJob, self).form_valid(form)



# @method_decorator([provider_required], name="dispatch")
class CompanyListView(ListView):
    template_name="JobFinderWeb/companylisting.html"
    
    def get_queryset(self, *args, **kwargs):
        slug = self.kwargs.get("slug")
        print(slug)
        if slug:
            try:
                querysetValue = Company.objects.filter(Q(category__iexact = slug) | Q(category__icontains = slug)
                )
                querysetValue2 = querysetValue.filter(IsActive=True)
            except querysetValue2.DoesNotExist:
                raise Http404("Company does not exists")
            queryset = querysetValue2

        elif 'cat' in self.request.GET or 'location' in self.request.GET:
            cat = self.request.GET.get('cat')
            loc = self.request.GET['location']
            if cat == "All Catgoery":
                queryset = Company.objects.filter(location__icontains = loc,IsActive = True)
            else:
                catlist = cat.split()
                # reduce(operator.and_, (Q(first_name__contains=x) for x in ['x', 'y', 'z']))
                queryset = Company.objects.filter(location__icontains = loc, category__icontains = cat, IsActive = True)
                # queryset = Company.objects.filter(reduce(operator.and_, (Q(category__icontains =x) for x in catlist)))
        else:
            queryset = Company.objects.filter(IsActive = True)
        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super(CompanyListView, self).get_context_data(*args, **kwargs)
        if self.request.GET.get('cat') is not None:
            context['cat'] = self.request.GET['cat']
            context['location'] = self.request.GET['location']
        else:
            context['cat'] = "All Categories"
        print(self.request.GET.getlist('cat'))
        return context


@method_decorator([provider_required], name="dispatch")
class CompanyJobList(LoginRequiredMixin,ListView):
    template_name = 'JobFinderWeb/companyjobs.html'

    def get_queryset(self, *args, **kwargs):
        queryset = Job.objects.filter(Company__IsActive=True, user = self.request.user, IsActive=True)
        return queryset
        

def DeleteCompany(request, slug):
    company = get_object_or_404(Company, slug = slug)
    company.IsActive= False
    company.save()
    messages.success(request, "Successfully Deactivated. You can contact the website admin to reactive it when needed")
    return HttpResponseRedirect('/provider/{}'.format(request.user.username))


def DeleteJob(request, slug):
    job = get_object_or_404(Job, slug = slug)
    job.IsActive= False
    job.save()
    messages.success(request, "Successfully Deactivated. You can contact the website admin to reactive it when needed")
    return HttpResponseRedirect('/{}/jobs'.format(request.user.username))


def logout(request):
    log_out(request)
    return HttpResponseRedirect('/')




