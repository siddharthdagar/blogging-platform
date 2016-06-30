from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt
from .views.posts import PostsView
from .views.postdetail import PostDetailView
from .views.postcomments import PostCommentView

urlpatterns = [
    # url(r'^$', csrf_exempt(PostsView()))
    url(r'^$', PostsView.as_view()),
    url(r'^(?P<post_uid>\w+)/?$', PostDetailView.as_view()),
    url(r'^(?P<post_uid>\w+)/comments/?$', PostCommentView.as_view()),
]
