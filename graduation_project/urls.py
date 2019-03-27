"""exam_system URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import include, url
from exam_system import tools_views
from exam_system import bbs_views
from . import settings
from django.views.static import serve

from django.conf.urls.static import static
#使用其他模块的东西要先import      as tool_views是为了区分不同模块的views
urlpatterns = [
    url(r'^start_exam/$', tools_views.start_exam, name='start_exam'),
    url(r'^get_psw/$', tools_views.get_psw, name='get_psw'),

    url(r'^event_manage/$', bbs_views.event_manage, name='event_manage'),
    #name=xxx是为了在html中直接引用，例如href="/xxx/"   替代了href="127.0.0.1/xxx/"
    url(r'^file/(?P<path>.*)$', serve, {'document_root':settings.MEDIA_ROOT}),
    url(r'^send_email/$', tools_views.send_email, name='send_email'),
    url(r'^data_in/$', tools_views.data_in, name='data_in'),
    url(r'^data_out/$', tools_views.data_out, name='data_out'),
    # url(r'^ajax/post/', tools_views.ajax_post,name='ajax/post'),
]
              #+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)  这种方法仅仅在debug模式下起作用
