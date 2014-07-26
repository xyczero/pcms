# -*-coding:utf-8 -*-
from __builtin__ import super
from datetime import  datetime

from django.contrib.auth.models import User
from django.db import models
from django.db.models.fields.related import ForeignKey
from markdown import markdown
from wmd import models as wmd_models


# Create your models here.
class Tag(models.Model):
    name = models.CharField(max_length=30)
    create_time = models.DateTimeField(auto_now_add=True)
    
    def __unicode__(self):
        return self.name
    
class Category(models.Model):
    name = models.CharField(max_length=30)
    create_time = models.DateTimeField(auto_now_add=True)
    
    def __unicode__(self):
        return self.name
    
class BlogManager(models.Manager):
    def title_count(self, keyword):
        return self.filter(title__icontains=keyword).count()

    def tag_count(self, keyword):
        return self.filter(tags__icontains=keyword).count()

    def author_count(self, keyword):
        return self.filter(author__icontains=keyword).count()  
    
class Blog(models.Model):
    title = models.CharField(max_length=50)
    author = ForeignKey(User)
    category = models.ForeignKey(Category,default='',related_name="blogs", related_query_name="blog")
    tags = models.ManyToManyField(Tag, blank=True, related_name="blogs", related_query_name="blog")
    content = wmd_models.MarkDownField(blank=True)
    content_html = models.TextField(blank=True)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now_add=True)
    is_release = models.BooleanField('Release right now?', default=False)
    
    objects = models.Manager()
    count_objects = BlogManager()
    
    is_release.short_description = 'Release right now?'
    
    def save(self):
        self.create_or_update_release()
        if not self.content_html: 
            self.content_html = markdown(self.content, ['codehilite'])
        super(Blog, self).save()
        for tag in self.tags.all():
            p, created = Tag.objects.get_or_create(name=tag.name, create_time=tag.create_time)
            if created:
                self.tags.add(p)

    def __unicode__(self):
        return u'%s %s %s' % (self.title, self.author, self.create_time)
    
    def create_or_update_release(self):
        if self.create_time:
            self.update_time = datetime.now()
            

            
