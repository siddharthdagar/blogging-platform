import json

from django.http import (HttpResponse, HttpResponseBadRequest,
                         HttpResponseNotAllowed)
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View

from base import utils
from blogentries.models import Post, PostComponent, Comment


@method_decorator(csrf_exempt, name='dispatch')
class PostCommentView(View):
    def get(self, request, *args, **kwargs):
        request = self.request

        result = {}
        post = get_object_or_404(Post, uid=kwargs['post_uid'])
        result['data'] = post.get_comments()

        resp_dict = {
            'message': '',
            'error': 0,
            'result': result
        }
        json_resp = json.dumps(resp_dict, cls=utils.CustomJsonEncoder)
        return HttpResponse(json_resp, content_type="application/json")

    def post(self, request, *args, **kwargs):
        request = self.request

        post = get_object_or_404(Post, uid=kwargs['post_uid'])
        try:
            req_body = utils.parse_request_body(request)
        except ValueError:
            return HttpResponseBadRequest("JSON couldn't be decoded")

        msg, resp, result = self.add_comment(post, req_body)
        if resp:
            return HttpResponseBadRequest(msg)

        resp_dict = {
            'message': '',
            'error': 0,
            'result': result
        }
        json_resp = json.dumps(resp_dict, cls=utils.CustomJsonEncoder)
        return HttpResponse(json_resp, content_type="application/json")

    def add_comment(self, post, data):
        '''
        Adds a comment for given post.
        Component id, text should be provided in data
        '''
        msg, resp, result = '', 0, {}
        mandatory_fields = ['component_id', 'text']
        if not all([data.get(i) for i in mandatory_fields]):
            resp = 400
            msg = "Fields missing"
            return msg, resp, result

        try:
            post_comp = PostComponent.objects.get(post=post, id=data['component_id'])
        except PostComponent.DoesNotExist:
            resp = 400
            msg = "Component not found for given post"
            return msg, resp, result

        comment_params = {
            'post_component': post_comp,
            'text': data['text']
        }

        comment_obj = Comment.objects.create(**comment_params)
        result['comment_id'] = comment_obj.id

        return msg, resp, result
