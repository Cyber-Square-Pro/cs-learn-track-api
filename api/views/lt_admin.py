from rest_framework.views import APIView
from django.http import HttpResponse


class LandingEndPoint(APIView):
    def get(self,request):
        return HttpResponse('<h1 align="center" style="margin-top:200px">Welcome Onboard!..</h1>')
