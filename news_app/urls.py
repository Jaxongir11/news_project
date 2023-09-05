from django.urls import path
from .views import NewsList, NewsDetail, IndexPageView, ContactView, \
    ErrorView, singlePageView, aboutView, LocalNewsView, ForeignNewsView, \
    SportNewsView, TechnologyNewsView, NewsUpdateView, NewsDeleteView
urlpatterns=[
    path('',IndexPageView.as_view(),name='index_page'),
    path('news/',NewsList.news_list,name='all_news_list'),
    path('news/<slug:slug>/',NewsDetail.as_view(),name='news_detail_page'),
    path('news/<slug>/edit/',NewsUpdateView.as_view(),name='update_news'),
    path('news/<slug>/delete/',NewsDeleteView.as_view(),name='delete_news'),
    path('contact/',ContactView.as_view(),name='contact_page'),
    path('404/',ErrorView,name='404_page'),
    path('single_page',singlePageView,name='single_page'),
    path('about/',aboutView,name='about_page'),
    path('local/',LocalNewsView.as_view(),name = 'local_page'),
    path('foreign/',ForeignNewsView.as_view(),name = 'foreign_page'),
    path('sport/',SportNewsView.as_view(),name = 'sport_page'),
    path('technology/',TechnologyNewsView.as_view(),name = 'technology_page'),
]