from django.urls import path
from projects.api.views import *


app_name = "project"
urlpatterns = [
    path('type/', ContentsView.as_view(), name='contents'),
    path('type/<name>', ContentFlagsView.as_view(), name='content_flags'),
    path('all/', AllProjectsListView.as_view(), name='all_projects'),
    # path('tags/', AllTagsListView.as_view(), name='all_tags'),
    # custom port's
    path('all/blog', CustomBlogContentView.as_view(), name='custom_blog'),
    # path('all/blog', CustomBlogContentView.as_view(), name='custom_blog'),
    # custom port's END
    path('create/', ContentCreateView.as_view(), name='project'),
    path('edit/', AdminAllProjectsListView.as_view(), name='admin-projects'),
    path('edit/<str:slug>/', ProjectRetrieveUpdateDestroyView.as_view(), name='project'),
    path('comment/<str:slug>/', CreateCommentView.as_view(), name='comment'),
    path('<str:slug>/', ProjectRetrieveView.as_view(), name='project'),
]

