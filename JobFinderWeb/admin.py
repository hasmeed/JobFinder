from django.contrib import admin
from .models import Seeker,Education,Experience,Skill,Provider,Company,Job,Resumee,Application,Identity,CustomJobApplication

admin.site.register(Seeker)
admin.site.register(Education)
admin.site.register(Experience)
admin.site.register(Provider)
admin.site.register(Company)
admin.site.register(Job)
admin.site.register(Resumee)
admin.site.register(Application)
admin.site.register(Skill)
admin.site.register(Identity)
admin.site.register(CustomJobApplication)