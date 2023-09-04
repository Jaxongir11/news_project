from django.shortcuts import render, get_object_or_404, HttpResponse
from django.views.generic import ListView, DetailView, TemplateView
from .models import News, Category
from .forms import ContactForm
# Create your views here.

class NewsList(ListView):
    def news_list(request):
        news_list = News.objects.filter(status=News.Status.published)
        context = {
            'news_list': news_list
                 }
        return render(request, 'news/news_list.html', context)

class NewsDetail(DetailView):
    model = News
    template_name = 'news/news_detail.html'

def indexView(request):
    categories = Category.objects.all()
    news = News.objects.filter(status=News.Status.published).order_by('-publish_time')[:5]
    local_one = News.objects.filter(status=News.Status.published).filter(category__name='Mahalliy').order_by('-publish_time')[0:1]
    local_news = News.objects.filter(status=News.Status.published).filter(category__name='Mahalliy').order_by('-publish_time')[1:6]
    context = {
        'news': news,
        'categories' : categories,
        'local_news' : local_news,
        'local_one' : local_one
    }
    return render(request, 'news/index.html', context)

class IndexPageView(ListView):
    model = News
    template_name = 'news/index.html'
    context_object_name = 'news'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['news'] = News.objects.filter(status=News.Status.published).order_by('-publish_time')[:5]
        context['local_one1'] = News.objects.filter(status=News.Status.published).filter(category__name='Mahalliy').order_by('-publish_time')[0:1]
        context['local_one2'] = News.objects.filter(status=News.Status.published).filter(category__name='Xorij').order_by('-publish_time')[0:1]
        context['local_one3'] = News.objects.filter(status=News.Status.published).filter(category__name='Sport').order_by('-publish_time')[0:1]
        context['local_one4'] = News.objects.filter(status=News.Status.published).filter(category__name='Texnologiya').order_by('-publish_time')[0:1]
        context['local_news1'] = News.objects.filter(status=News.Status.published).filter(category__name='Mahalliy').order_by('-publish_time')[1:6]
        context['local_news2'] = News.objects.filter(status=News.Status.published).filter(category__name='Xorij').order_by('-publish_time')[1:6]
        context['local_news3'] = News.objects.filter(status=News.Status.published).filter(category__name='Sport').order_by('-publish_time')[1:6]
        context['local_news4'] = News.objects.filter(status=News.Status.published).filter(category__name='Texnologiya').order_by('-publish_time')[1:6]
        return context

class ContactView(TemplateView):
    template_name = 'news/contact.html'

    def post(self, request, *args, **kwargs):
        form = ContactForm(request.POST)
        if request.method == 'POST' and form.is_valid():
            form.save()
            return HttpResponse("<h2>Biz bilan bog'langaningiz uchun raxmat! </h2>")
        context = {
            'form': form
        }
        return render(request, 'news/contact.html', context)

def ErrorView(request):
    context = {

    }
    return render(request, 'news/404.html', context)

def singlePageView(request):
    context = {

    }
    return render(request, 'news/single_page.html', context)

def aboutView(request):
    context = {

    }
    return render(request, 'news/about.html', context)

class LocalNewsView(ListView):
    model = News
    template_name = 'news/local_page.html'
    context_object_name = 'local_page'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['local_news'] = News.objects.filter(status=News.Status.published).filter(category__name='Mahalliy').order_by('-publish_time')
        return context

class ForeignNewsView(ListView):
    model = News
    template_name = 'news/foreign_page.html'
    context_object_name = 'foreign-page'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['local_news'] = News.objects.filter(status=News.Status.published).filter(category__name='Xorij').order_by('-publish_time')
        return context

class SportNewsView(ListView):
    model = News
    template_name = 'news/sport_page.html'
    context_object_name = 'sport-page'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['local_news'] = News.objects.filter(status=News.Status.published).filter(category__name='Sport').order_by('-publish_time')
        return context

class TechnologyNewsView(ListView):
    model = News
    template_name = 'news/technology_page.html'
    context_object_name = 'technology-page'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['local_news'] = News.objects.filter(status=News.Status.published).filter(category__name='Texnologiya').order_by('-publish_time')
        return context
