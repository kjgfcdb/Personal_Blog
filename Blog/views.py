import hashlib
import json
import re

from django.contrib.auth import login, logout, REDIRECT_FIELD_NAME
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import AnonymousUser
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.generic import TemplateView, FormView

from .forms import UserForm
from .models import *


# TODO:注册之后跳转问题

# Create your views here.
def blogs(request):
    return render(request, 'Blog/index.html', context={
        'blogs': Blog.objects.order_by('created_at')[::-1]
    })


def signout(request):
    # delete the user
    logout(request)
    return HttpResponseRedirect("/")



def signin(request):
    # return HttpResponse("Register")
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        if user_form.is_valid():
            user_email = user_form.cleaned_data['email']
            user_passwd = user_form.cleaned_data['passwd']
            users = User.objects.filter(
                email=user_email
            )
            if users.__len__() == 0:
                raise Exception("Email doesn't exist.")
            sha1 = hashlib.sha1()
            sha1.update(user_email.encode('utf-8'))
            sha1.update(b':')
            sha1.update(user_passwd.encode('utf-8'))
            if users[0].password == sha1.hexdigest():
                # response = render(request, 'Blog/index.html', context={
                #     'blogs': Blog.objects.order_by(
                #         'created_at'
                #     )[::-1]
                # })
                login(request,users[0])
                # response.set_cookie('user', user2cookie(users[0], 3600), max_age=3600, httponly=True)
                return HttpResponseRedirect("/")
            else:
                return HttpResponseRedirect("/")
        # print(request.POST['name'])
        # User(name=user_data['name'], email=user_data['email'], passwd=user_data['passwd']).save()
        return HttpResponse("<h1>404 Not Found</h1>")
    else:
        return render(request, 'Blog/signin.html', content_type='text/html')


def register(request):
    # return HttpResponse("Register")
    if request.method == 'POST':
        # 返回的是一个json格式数据，需要用json解析
        user_data = json.loads(request.body.decode('utf-8'))
        new_user = User(name=user_data['name'], email=user_data['email'], password=user_data['passwd'])
        new_user.save()
        return render(request, 'Blog/index.html', context={
        })
    else:
        return render(request, 'Blog/register.html', content_type='text/html')


def create_blog(request):
    # blog = Blog(user_id=request.__user__.id, user_name=request.__user__.name, user_image=request.__user__.image,
    #             name=name.strip(), summary=summary.strip(), content=content.strip())
    # blog.save()
    if request.method == "POST":
        blog_data = json.loads(request.body.decode('utf-8'))
        new_blog = Blog(name=blog_data['name'], summary=blog_data['summary'], content=blog_data['content'])
        new_blog.save()
        return HttpResponseRedirect("/")
    else:
        return render(request, 'Blog/create_blog.html')


def show_blog(request):
    blog_id = re.findall(r'/blogs/(.*?)/', request.path)[0]
    blogs = Blog.objects.filter(
        id__exact=blog_id
    )
    # return HttpResponse("Name:%s\tSummary:%s\tContent:%s"%(blogs[0].name,blogs[0].summary,blogs[0].content))
    return render(request, 'Blog/blog.html', context={
        'blog': blogs[0]
    })


def add_comment(request):
    if request.method=="POST":
        # /blogs/0015019890947914d0e05dd598a440fb23e1d0e0f7a2b8e000/comments/
        blog_id = re.findall(r'blogs/([0-9a-zA-Z]+)/comments/',request.path)[0]
        content = json.loads(request.body.decode('utf-8'))['content']
        blog = Blog.objects.filter(
            id=blog_id
        )[0]
        Comment.objects.create(user_name = request.user.name,blog=blog,content=content)
        return HttpResponse()
    else:
        return HttpResponse()
