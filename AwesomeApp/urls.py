"""AwesomeApp URL Configuration

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

from Blog import views

urlpatterns = [
    url(r'^$', views.blogs, name='index'),
    url(r'^admin/', admin.site.urls),
    url(r'^register/$', views.register, name='register'),
    url(r'^signout/$', views.signout, name='signout'),
    url(r'^signin/$', views.signin, name='signin'),
    url(r'^create_blogs/$', views.create_blog, name='create_blog'),
    url(r'^blogs/', include('Blog.urls')),
    url(r'^blogs/[0-9a-zA-Z]+/$', views.show_blog, name='show_blog'),
    url(r'^blogs/[0-9a-zA-Z]+/comments/$', views.add_comment, name='add_comment')
]
