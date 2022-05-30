from django.shortcuts import render
from django.http import HttpResponse,Http404,HttpResponseRedirect
from .models import Question,Choice,Article,Classification,Comment,Tag
from django.template import loader
from django.shortcuts import render,get_object_or_404
from django.urls import reverse
from django.views import generic
from django.utils.text import slugify
from markdown.extensions.toc import TocExtension
import markdown
import re


# 通用视图ListView和DetailView
class IndexView(generic.ListView):
    # template_name 默认值为app name/model name
    template_name = 'polls/templates/index.html_temp'
    # context_object_name 默认变量为model_list,ex:question_list
    context_object_name = ''

    def get_queryset(self):
        return Question.objects.order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


# Create your views here.
# def index(request):
#     latest_question_list = Question.objects.order_by('-pub_date')[:5]
#     # output = ', '.join([q.question_text for q in latest_question_list])
#     template = loader.get_template('polls/templates/index.html_temp')
#     context = {
#         'latest_question_list': latest_question_list,
#     }
#     # return HttpResponse(template.render(context, request))
#     return render(request, 'polls/templates/index.html_temp', context)

def detail(request,question_id):
    # try:
    #     question = Question.objects.get(pk=question_id)
    # except Question.DoesNotExist:
    #     raise Http404("Question does not exist")

    # 快捷函数
    question = get_object_or_404(Question,pk=question_id)
    return render(request,'polls/detail.html',{'question':question})


# results 视图与index视图代码重复，将通过引入通用视图进行改善
def results(request,question_id):
    question = get_object_or_404(Question,pk=question_id)
    return render(request,'polls/results.html',{'question':question})


def vote(request,question_id):
    question = get_object_or_404(Question,pk=question_id)
    try:
        print("here")
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
        print(selected_choice)
    except (KeyError, Choice.DoesNotExist):
        return render(request,'polls/detail.html',{'question':question,'error_message':"You didn't select a choice"})
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results',args=(question.id,)))


    # return HttpResponse("You're voting on question %s." % question_id)

#  Modified the index.html_temp
# 2022/05/23 15:40
def index(request):
    article_list = Article.objects.all()
    context = {
        'article_list':article_list
    }
    return render(request, 'polls/index.html', context)


def articleDetail(request,article_id):
    # print(article_id)
    article = get_object_or_404(Article,pk=article_id)
    md = markdown.Markdown(extensions=[ 'markdown.extensions.extra','markdown.extensions.codehilite',
        'markdown.extensions.tables',
        'markdown.extensions.wikilinks',TocExtension(slugify=slugify),])
    content_body = md.convert(article.content)
    m = re.search(r'<div class="toc">\s*<ul>(.*)</ul>\s*</div>',md.toc,re.S)
    article.toc = m.group(1) if m is not None else ' '
    return render(request,'polls/articleDetail.html',{'article':article,'content_body':content_body})



def archive(request,year,month):
    article_list = Article.objects.filter(pub_date__year=year,pub_date__month=month).order_by('-pub_date')
    return render(request,'polls/index.html',{'article_list':article_list})


def classification(request,pk):
    classification_name = get_object_or_404(Classification,pk=pk)
    article_list = Article.objects.filter(classification=classification_name).order_by('-pub_date')
    return render(request,'polls/classification.html',{'article_list':article_list})

def tags(request,pk):
    tag = get_object_or_404(Tag,pk=pk)
    article_list = Article.objects.filter(tags=tag).order_by('-pub_date')
    return render(request,'polls/tags.html',{'article_list':article_list})