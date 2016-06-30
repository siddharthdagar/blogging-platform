import json

from django.http import HttpResponse, HttpResponseNotAllowed
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View

from base import utils
from blogentries.models import Post


@method_decorator(csrf_exempt, name='dispatch')
class PostDetailView(View):
    def get(self, request, *args, **kwargs):
        request = self.request

        result = {}
        post = get_object_or_404(Post, uid=kwargs['post_uid'])
        fetch_comments = request.GET.get('fetch_comments', False)
        try:
            fetch_comments = int(fetch_comments)
        except ValueError:
            fetch_comments = False
        result['data'] = post.get_details(fetch_comments=fetch_comments)

        resp_dict = {
            'message': '',
            'error': 0,
            'result': result
        }
        json_resp = json.dumps(resp_dict, cls=utils.CustomJsonEncoder)
        return HttpResponse(json_resp, content_type="application/json")
