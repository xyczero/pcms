# -*-coding:utf-8 -*-
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render

from blog.models import Blog, Tag, Category


# Create your views here.
def index(request, ct_name):
    if ct_name.lower() == 'home':
        page_num = 5
        is_ct = False
        blog_list = Blog.objects.filter(is_release=True).order_by('-create_time')
    else:
        page_num = 5
        is_ct = True
        blog_list = Blog.objects.filter(category__name=ct_name, is_release=True).order_by('-create_time')
        if not blog_list:
            tag=Tag.objects.filter(name=ct_name)
            if tag :
                tag[0].clicks=int(tag.clicks)+1
                tag[0].save()
            blog_list = Blog.objects.filter(tags__name=ct_name, is_release=True).order_by('-create_time')
            
    blogs = blog_paginator(request, blog_list, page_num)    
    categories, new_blogs, date_archive_list = get_aside_init()
    return render(request, 'blog/blog_list.html', 
                  {'blogs':blogs, 
                   'new_blogs':new_blogs,
                   'categories':categories, 
                   'tags':Tag.objects.all(), 
                   'date_archive_list':date_archive_list, 
                   'is_ct':is_ct, 
                   }) 

def article(request, article_id):
    blog = Blog.objects.get(id=int(article_id), is_release=True)
        
    categories, new_blogs, date_archive_list = get_aside_init()
    return render(request, 'blog/blog_article.html', {'blog':blog, 
                                                      'new_blogs':new_blogs, 
                                                      'categories':categories, 
                                                      'tags':Tag.objects.all(), 
                                                      'date_archive_list':date_archive_list, 
                                                      })


def archive(request, published_year, published_month):
#     blogs = Blog.objects.filter(create_time__year=published_year,create_time__month=published_month,is_release=True)  
    blogs = []
    for blog in Blog.objects.all():
        if  str(blog.create_time.year) == published_year and  str(blog.create_time.month) == published_month and blog.is_release == True:
            blogs.append(blog)
    categories, new_blogs, date_archive_list = get_aside_init()
    return render(request, 'blog/blog_archive.html', {'blogs':blogs, 
                                                      'new_blogs':new_blogs, 
                                                      'categories':categories, 
                                                      'tags':Tag.objects.all(), 
                                                      'date_archive_list':date_archive_list, 
                                                      'published_year':published_year, 
                                                      'published_month':published_month, 
                                                      })

def about(request):
    categories, new_blogs, date_archive_list = get_aside_init()
    return render(request, 'blog/about.html', {'new_blogs':new_blogs, 
                                               'categories':categories, 
                                               'tags':Tag.objects.all(), 
                                               'date_archive_list':date_archive_list, 
                                               })

def blog_paginator(request, blog_list, page_num):
    paginator = Paginator(blog_list, page_num)
    page = request.GET.get('page')
    try:
        blogs = paginator.page(page)
    except PageNotAnInteger:
        blogs = paginator.page(1)
    except EmptyPage:
        blogs = paginator.page(paginator.num_pages) 
    return blogs

def get_aside_init():
    categories = Category.objects.all()
    blogs = Blog.objects.filter(is_release=True).order_by('-create_time');
    return categories, blogs[0:5], get_archive_date(blogs)

def get_archive_date(blogs):
    years = []
    month_list = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"]
    for blog in blogs:
        if not years.__contains__(blog.create_time.year):
            years.append(blog.create_time.year)
    date_archive_list = [(["/"] * 13) for i in range(len(years))]
    for x in range(len(years)):
        date_archive_list[x][0] = years[x]
    for x in range(len(years)):
        for y in range(len(month_list)):
            for blog in blogs:
                if blog.create_time.year == years[x] and str(blog.create_time.month) == month_list[y] and date_archive_list[x][y + 1] == "/":
                        date_archive_list[x][y + 1] = month_list[y]
    return date_archive_list
