"""coldmaterWeb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns

from coldmaterhttp import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)

urlpatterns = [        
    #url(r'^userList/$', views.user_list4.as_view())
    #url(r'^userList/(?P<pk>[0-9]+)/$', views.user_details4.as_view())
    url(r'^', include(router.urls)),
    url(r'^user/username=(?P<username>\w+)&password=(?P<password>\w+)/', views.check_login),
    url(r'^login/', views.login_form, name='login_form'),
    url(r'^dashboard/(?P<userid>\w+)', views.dashboard, name='dashboard'),
    url(r'^logout/', views.logout, name='logout'),
	#url(r'^$', views.index, name='index'),
	#url(r'^user/(?P<id>\d+)/', views.user_detail, name='user_detail'),
    url(r'^admin/', admin.site.urls),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]

#urlpatterns = format_suffix_patterns(urlpatterns)