from django.urls import path
from core.views import *

urlpatterns = [
    path("login/", LoginApiView.as_view(), name='login'),
    path("logout/", LogoutApiView.as_view(), name='logout'),
    path("blog/list/v1/", BlogListApiView.as_view(), name='blog_list'),
    path("blog/v1/", BlogCreateApiView.as_view(), name='blog_create'),
    path("blog/<int:pk>/v1/", BlogRetrieveApiView.as_view(), name='blog_retrieve'),
    path("blog/<int:pk>/v1/update/", BlogUpdateDeleteApiView.as_view(), name='blog_update_delete'),
    path("comments/v1/", BlogCommentsCreateApiView.as_view(), name='comments_create'),

]