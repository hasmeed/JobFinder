from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from rest_framework_jwt.settings import api_settings
from rest_framework_jwt.utils import jwt_payload_handler, jwt_encode_handler

# payload_handler = api_settings.JWT_PAYLOAD_HANDLER
# encode_handler = api_settings.JWT_ENCODE_HANDLER

payload_handler = jwt_payload_handler
encode_handler = jwt_encode_handler



from rest_framework.reverse import reverse as api_reverse
from rest_framework import status

from JobFinderWeb.models import Job, Company, Provider


User = get_user_model()

class JobAPITestCase(APITestCase):
    def setUp(self):
        user_obj = User(username = 'test', email='test@test.com')
        user_obj.set_password("testpass")
        user_obj.save()

        provider = Provider(identity = user_obj)
        provider.save()
        company = Company.objects.create(provider = provider, companyname='microsoft', user = user_obj)


        job_obj = Job.objects.create(user = user_obj, 
                                    jobtitle = 'test', Company = company)

    # def test_single_job(self):
    #     job_count = Job.objects.count()
    #     self.assertEqual(job_count, 1)

    # def test_single_user(self):
    #     user_count = User.objects.count()
    #     self.assertEqual(user_count, 1)

    def test_user(self):
        user_count = User.objects.count()
        self.assertEqual(user_count, 1)

    def test_get_job_list(self): # get list of jobs
        data = {}
        url = api_reverse("JobApi:listjob")
        response = self.client.get(url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_job(self): # get a single job
        job = Job.objects.first()
        data = {}
        url = job.get_api_url()
        response = self.client.get(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # def test_update_job(self):
    #     job = Job.objects.first()
    #     data = {"jobtitle":"Job 2", "Company":Company.objects.first()}
    #     url = job.get_api_url()
    #     user1 =  User.objects.first()
    #     payload = payload_handler(user1)
    #     token_rsp = encode_handler(payload)
    #     self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token_rsp)
    #     response = self.client.put(url, data)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     # print(data)


    def test_job_ownership(self):
        owner = User.objects.create(username="test222")
        job = Job.objects.create(user = owner, 
                                    jobtitle = 'another job', Company = Company.objects.first())


        user_obj = User.objects.first()
        payload = payload_handler(user_obj)
        token = encode_handler(payload)
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)

        data = {"jobtitle":"Job 2", "Company":Company.objects.first()}
        url = job.get_api_url()

        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        print(data)

        


    def test_post_job(self): # Post job
        data = {"user":get_object_or_404(User, username='test'), "jobtitle":"Job 2"}
        url = api_reverse("JobApi:listjob")
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)



    def test_login(self):
        data = {
            'username':'test',
            'password':'testpass'
        }
        url = api_reverse('JobApi:api-login')
        respone = self.client.post(url, data)
        print(respone.data)
        self.assertEqual(respone.status_code, status.HTTP_200_OK)
        token = respone.data.get("token")
        