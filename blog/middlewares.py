from django.utils.deprecation import MiddlewareMixin
from django.db.models.query import RawQuerySet

class printmiddleware(MiddlewareMixin):
    def process_request(self,request):
        messenge=f'user{request.user}\nrequest{request}\nmethod{request.method}\nGET{request.GET}\nPOST{request.POST}'
        print(messenge)