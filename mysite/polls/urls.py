from django.urls import path
from . import views

app_name = 'polls'
urlpatterns = [
    # path('<int:question_id>/',views.detail,name="detail"),
    # path('<int:question_id>/results/',views.results,name='results'),

    # 引入通用视图
    # path('',views.IndexView.as_view(),name='index'),
    # path('<int:pk>/',views.DetailView.as_view(),name='detail'),
    path('<int:pk>/results',views.ResultsView.as_view(),name='results'),
    # ex /polls/5/vote/
    path('<int:question_id>/vote/', views.vote, name='vote'),

    # Article urlpatterns
    path('', views.index, name='index'),
    path('<int:article_id>/',views.articleDetail,name='articleDetail'),
    path('archive/<int:year>/<int:month>/',views.archive,name='archive'),
    path('classification/<int:pk>/',views.classification,name='classification'),
    path('tag/<int:pk>/',views.tags,name='tags')
]

