from django.shortcuts import render
from django.http import HttpResponse

import json

# Create your views here.
def posts_view(request):
    resp_dict = {'message': "All fine", 'error': 0, 'result': {}}
    return HttpResponse(json.dumps(resp_dict), content_type="application/json")
