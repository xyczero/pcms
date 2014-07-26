from django.contrib import admin

from blog.models import Blog, Tag, Category


# Register your models here.
      
class BlogAdmin(admin.ModelAdmin):
    fieldsets = [
              ('Release', {'fields':['is_release']}),
              ('Category', {'fields':['category']}),
              ('Tags', {'fields':['tags',],'classes': ['collapse']}),
              ('Blog', {'fields':['title', 'author','content','content_html']}),
         ]
    list_display = ('title', 'author', 'create_time', 'update_time', 'is_release')
    list_filter = ('create_time',)
    ordering = ('-create_time',)
    filter_horizontal = ('tags',)
    raw_id_fields = ('author',)
#     exclude = ('content_html',)
    
    
    
admin.site.register(Blog, BlogAdmin)
admin.site.register(Tag)
admin.site.register(Category)
