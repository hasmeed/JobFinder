from django import forms
from .validators import username_validate

from django.forms.models import inlineformset_factory

from .models import Seeker,Education,Experience,Skill,Provider,Company,Job,Resumee,Application,Identity,CustomJobApplication


class SignUpForm(forms.Form):
    username = forms.CharField(max_length=120,
        widget=forms.TextInput(attrs={'placeholder':'Username'}))
    firstname = forms.CharField(max_length=120,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'First Name'}))
    lastname = forms.CharField(max_length=120,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Last Name'}))
    email = forms.CharField(max_length=120,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder':'Password'}))

class LoginForm(forms.Form):
    username = forms.CharField(max_length=120,
        widget=forms.TextInput(attrs={'placeholder':'Username'}), validators=[username_validate])
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder':'Password'}))


class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        exclude = ('provider',)
        fields = '__all__'


class CustomApplicationForm(forms.ModelForm):
    name = forms.CharField(max_length=120,
        widget=forms.TextInput(attrs={'class':'form-control input-lg','placeholder':'Name'}))

    email = forms.CharField(max_length=120,
        widget=forms.TextInput(attrs={'class':'form-control input-lg','placeholder':'Email'})) 
    
    message = forms.CharField(widget= forms.Textarea(attrs={'class':'form-control','placeholder':'Message', 'rows':'7'}))

    class Meta:
        model = CustomJobApplication
        exclude = ('application',)
        fields = '__all__'


class JobForm(forms.ModelForm):
    Company = forms.ModelChoiceField(queryset = Company.objects.all(), widget=forms.Select(attrs={'class':'form-control selectpicker'}))

    class Meta:
        model = Job
        exclude = ('slug',)
        fields = '__all__'
 
    def __init__(self, user=None, *args, **kwargs):
        super(JobForm, self).__init__(*args, **kwargs)
        self.fields['Company'] = forms.ModelChoiceField(queryset = Company.objects.filter(provider = user, IsActive=True), widget=forms.Select(attrs={'class':'form-control selectpicker'}))
        self.fields['Company'].empty_label = None


class ResumeeForm(forms.ModelForm):
    class Meta:
        model = Resumee
        exclude = ('owner','status')
        fields = '__all__'



EducationFormSet = inlineformset_factory(Resumee,  Education, exclude=['owner','resumee'], fields='__all__', extra=1,
                    widgets={'degree': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Degree, e.g. Bachelor'}),
                            'major': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Major, e.g. Computer Science'}),
                            'school': forms.TextInput(attrs={'class': 'form-control','placeholder': 'School name, e.g. Massachusetts Institute of Technology'}),
                            'datefrom': forms.TextInput(attrs={'class': 'form-control','placeholder': 'e.g. 2012'}),
                            'dateto': forms.TextInput(attrs={'class': 'form-control','placeholder': 'e.g. 2016'}),
                            'shortdescription': forms.Textarea(attrs={'class': 'form-control','placeholder': 'Short description', 'rows':'3'})
                            })

ExperienceFormSet = inlineformset_factory(Resumee, Experience, exclude=['owner','resumee'], fields='__all__', extra=1,
                    widgets={'companyname': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Company name'}),
                            'position': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Position, e.g. UI/UX Researcher'}),
                            'datefrom': forms.TextInput(attrs={'class': 'form-control','placeholder': 'e.g. 2012'}),
                            'dateto': forms.TextInput(attrs={'class': 'form-control','placeholder': 'e.g. 2016'}),
                            'description': forms.Textarea(attrs={'class': 'summernote-editor'})
                            })

SkillFormSet = inlineformset_factory(Resumee, Skill, exclude=['owner','resumee'], fields='__all__', extra=1,
                    widgets={'skillname': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Skill name, e.g. HTML'}),
                            'proficiency': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Skill proficiency, e.g. 90'}),
                            })

        