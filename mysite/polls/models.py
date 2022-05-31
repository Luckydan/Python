import datetime
from django.db import models
from django.utils import timezone
from django.utils.html import strip_tags
from django.urls import reverse
import random
import markdown

# Create your models here.
class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

class Choice(models.Model):
    question = models.ForeignKey(Question,on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text

class Tag(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = '标签'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

class User(models.Model):
    user_name = models.CharField(max_length=20)

    def __str__(self):
        return self.user_name


class Classification(models.Model):
    name = models.CharField('分类名称',max_length=100)

    def __str__(self):
        return self.name


class Article(models.Model):
    title = models.CharField('标题',max_length=100)
    introduction = models.CharField('简介',max_length=500,blank=True)
    content = models.TextField(default='暂无内容')
    classification = models.ForeignKey(Classification,on_delete=models.CASCADE)
    readCount = models.IntegerField(default=0)
    commentCount = models.IntegerField(default=0)
    # It must be in "YYYY-MM-DD HH:MM[:ss[.uuuuuu]][TZ]"
    author = models.CharField(verbose_name='作者',max_length=20)
    tags = models.ManyToManyField(Tag,verbose_name='标签',blank=True)
    pub_date = models.DateTimeField('date published',default=timezone.now)
    modified_time = models.DateTimeField(verbose_name="修改时间")

    class Meta:
        verbose_name = '文章'
        verbose_name_plural = verbose_name

    def save(self,*args,**kwargs):
        self.modified_time = timezone.now()

        # 去除目录渲染
        md = markdown.Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
        ])

        # strip_tags 去掉 HTML 文本的全部 HTML 标签,取54个字符作文简介
        self.introduction = strip_tags(md.convert(self.content))[:54]

        super(Article, self).save(self,*args,**kwargs)

    def __str__(self):
        return self.title



class ArticleDetail(models.Model):
    article = models.ForeignKey(Article,on_delete=models.CASCADE)
    content = models.TextField()

    # 后台汉化
    class Meta:
        verbose_name = '文章内容'
        verbose_name_plural = verbose_name



class Comment(models.Model):
    article = models.ForeignKey(Article,on_delete=models.CASCADE)
    comment_text = models.CharField(max_length=200)
    comment_pub_date = models.DateTimeField('comment published')
    name = models.CharField(verbose_name='名称',max_length=100,default="用户%s" %random.randrange(100))
    url =  models.URLField('网站',blank=True)
    email = models.EmailField('邮箱')

    def __str__(self):
        return '{}: {}'.format(self.name, self.comment_text[:20])

    class Meta:
        verbose_name = '评论'
        verbose_name_plural = verbose_name

