from __future__ import unicode_literals

from django.db import models
from django.utils import timezone

# Create your models here.

class Post(models.Model):
    uid     = models.CharField(max_length=128, unique=True)
    title   = models.CharField(max_length=200)
    dt_added = models.DateTimeField(default=timezone.now)

    def __unicode__(self):
        return "Title: %s" % self.title

    def get_details(self, fetch_comments=False):
        '''
        Gets all the details of the post along with all components
        '''

        post_dict = dict()
        fields = ['uid', 'title', 'dt_added']
        for field in fields:
            if hasattr(self, field):
                post_dict[field] = getattr(self, field)

        comps = self.postcomponent_set.order_by('order_rank')\
                                      .values()

        if fetch_comments:
            comments = self.get_comments()
            comments_dict = dict()
            for comment in comments:
                p_comp_id = comment['component_id']
                comments_dict.setdefault(p_comp_id, [])
                comments_dict[p_comp_id].append(comment)

            for comp in comps:
                if comments_dict.get(comp['id']):
                    comp['comments'] = comments_dict[comp['id']]

        post_dict['components'] = list(comps)

        return post_dict

    def get_comments(self):
        '''
        Gets all the comments of the post
        '''
        comments = self.postcomponent_set.filter(comment__id__isnull=False)\
                                         .values('id', 'comment__id',
                                                 'comment__text')
        field_name_map = {
            'id': 'component_id',
            'comment__id': 'id',
            'comment__text': 'text'
        }
        temp_comments = list(comments)
        comments = []
        for item in temp_comments:
            temp_d = {}
            for key, val in field_name_map.iteritems():
                temp_d[val] = item[key]
            comments.append(temp_d)

        return comments

class PostComponent(models.Model):
    post    = models.ForeignKey(Post)
    comp_type_choices = ((1, 'Paragraph'),)
    comp_type = models.IntegerField(choices=comp_type_choices)
    text = models.TextField()
    order_rank = models.IntegerField(default=1)
    dt_added = models.DateTimeField(default=timezone.now)

    def __unicode__(self):
        return "Id: %s, Post: %s, Type: %s, Order Rank: %s" % (self.id, self.post,
                                                               self.get_comp_type_display(),
                                                               self.order_rank)


class Comment(models.Model):
    post_component = models.ForeignKey(PostComponent)
    text = models.TextField()
    dt_added = models.DateTimeField(default=timezone.now)
