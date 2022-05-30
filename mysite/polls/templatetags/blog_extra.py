from django import template
from ..models import Article,Tag,Classification

register = template.Library()

# 模板标签，通过templage.Library() 和 register.inclusion_tag()装饰器函数来实现模板渲染
@register.inclusion_tag(filename='polls/inclusions/_recent_posts.html',takes_context=True)
def show_recent_blogs(context,num=5):
    return {
        'recent_blog_list':Article.objects.all().order_by('-pub_date')[:num],
    }


@register.inclusion_tag(filename='polls/inclusions/_archives.html',takes_context=True)
def show_archives(context):
    return {
        'date_list':Article.objects.dates('pub_date','month',order='DESC'),
    }


@register.inclusion_tag(filename='polls/inclusions/_categories.html',takes_context=True)
def show_categories(context):
    return {
        'classification_list':Classification.objects.all()
    }


@register.inclusion_tag(filename='polls/inclusions/_tags.html',takes_context=True)
def show_tags(context):
    return {
        'tag_list':Tag.objects.all()
    }
