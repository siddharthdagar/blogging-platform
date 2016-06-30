import json
import uuid
from itertools import groupby

from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db import transaction
from django.http import (HttpResponse, HttpResponseBadRequest,
                         HttpResponseNotAllowed)
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View

from base import utils
from blogentries.models import Post, PostComponent


@method_decorator(csrf_exempt, name='dispatch')
class PostsView(View):
    def get(self, request, *args, **kwargs):
        '''
        Get list of posts
        '''
        request = self.request
        result = {'data': []}

        page = request.GET.get('page')
        size = request.GET.get('size')
        if page:
            if size:
                posts_result = self.get_posts(page, size)
            else:
                posts_result = self.get_posts(page)
        else:
            posts_result = self.get_posts()

        resp_dict = {
            'message': '',
            'error': 0,
            'result': posts_result
        }
        return HttpResponse(json.dumps(resp_dict), content_type="application/json")

    def post(self, request, *args, **kwargs):
        '''
        Add a post
        '''
        request = self.request
        try:
            req_body = utils.parse_request_body(request)
        except ValueError:
            return HttpResponseBadRequest("JSON couldn't be decoded")

        msg, resp, result = self.add_post(req_body)
        if resp:
            return HttpResponseBadRequest(msg)

        resp_dict = {
            'message': msg,
            'error': resp,
            'result': result
        }
        return HttpResponse(json.dumps(resp_dict), content_type="application/json")

    def get_posts(self, page=None, size=5):
        result = {}
        posts = []
        posts_qs = Post.objects.all().order_by('id').values('id', 'uid', 'title')

        posts_paginator = Paginator(posts_qs, size)
        result['pagination_info'] = {
            'per_page': posts_paginator.per_page,
            'num_pages': posts_paginator.num_pages
        }
        if not page:
            posts = list(posts_qs)
        else:
            try:
                posts = list(posts_paginator.page(page))
            except PageNotAnInteger:
                posts = list(posts_paginator.page(1))
            except EmptyPage:
                # Last page if index out of range
                posts = list(posts_paginator.page(posts_paginator.num_pages))

        post_ids = [post['id'] for post in posts]
        post_comps = PostComponent.objects.filter(post_id__in=post_ids)\
                                          .order_by('post_id', 'order_rank')\
                                          .values('post__uid', 'post__title',
                                                  'text')

        post_comps = list(post_comps)
        posts = []
        for uid, vals in groupby(post_comps, lambda x: x['post__uid']):
            vals = list(vals)
            post_data = {'uid': uid, 'title': vals[0]['post__title']}
            post_data['text'] = '\n\n'.join(val['text'] for val in vals)
            posts.append(post_data)

        result['data'] = posts
        

        return result

    def add_post(self, data):
        '''
        Adds a post
        '''
        msg, resp, result = '', 0, {}
        mandatory_fields = ['title', 'text']
        if not all([data.get(i) for i in mandatory_fields]):
            resp = 400
            msg = "Fields missing"
            return msg, resp, result

        para_comps = [i.strip() for i in data['text'].split('\n\n')]

        with transaction.atomic():
            post_params = {
                'uid': str(uuid.uuid4()).replace('-', ''),
                'title': data['title']
            }

            post = Post.objects.create(**post_params)

            for index, p_comp in enumerate(para_comps):
                comp_params = {
                    'post': post,
                    'comp_type': 1, # Paragraph
                    'text': p_comp,
                    'order_rank': index + 1
                }
                post_comp = PostComponent.objects.create(**comp_params)

            result['post_uid'] = post.uid

        return msg, resp, result
