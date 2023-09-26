from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, HttpResponse
from django.urls import reverse_lazy
from django.utils.text import slugify
from django.views.generic import ListView, DetailView, TemplateView, UpdateView, DeleteView, CreateView
from hitcount.utils import get_hitcount_model
from hitcount.views import HitCountMixin

from .models import News, Category, Comment
from .forms import ContactForm, CommentForm
from news_project.custom_permissions import OnlyLoggedSuperuser
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

    def get_queryset(self):
        queryset = super(NewsDetail, self).get_queryset()
        post=News.objects.filter(status=News.Status.published)
        comments=Comment.objects.filter(post=post)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(NewsDetail, self).get_context_data(**kwargs)
        if request.method == "POST":
            comment_form = CommentForm(request.POST or None)
            if comment_form.is_valid():
                comment=comment_form.save(commit=False)
                comment.post = post
                comment.save()
        else:
            comment_form = CommentForm()
        context['post'] = post.objects.all()
        context['comments'] = comments.objects.all()
        context['comment_form'] = comment_form
        template_name = 'news/news_detail.html'
        return render(request, template_name, context)

def news_detail(request,slug):
    news = get_object_or_404(News,slug=slug,status=News.Status.published)
    comments = news.comments.filter(active=True)
    comment_count = comments.count()
    new_comment = None
    

    #hit count
    context = {}
    hit_count = get_hitcount_model().objects.get_for_object(news)
    hits = hit_count.hits
    hitcontext = context['hitcount'] = {'pk':hit_count.pk}
    hit_count_response = HitCountMixin.hit_count(request, hit_count)
    if hit_count_response.hit_counted:
        hits = hits + 1
        hitcontext['hit_counted'] = hit_count_response.hit_counted
        hitcontext['hit_message'] = hit_count_response.hit_message
        hitcontext['total_hits'] = hits


    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.news = news
            new_comment.user = request.user
            new_comment.save()
            comment_form = CommentForm()
    else:
        comment_form = CommentForm()
    context = {
        'news': news,
        'comments': comments,
        'comment_count':comment_count,
        'new_comment': new_comment,
        'comment_form': comment_form
    }
    return render(request,'news/news_detail.html',context)

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

class NewsUpdateView(OnlyLoggedSuperuser, UpdateView):
    model = News
    fields = ['title', 'body', 'image', 'category', 'status']
    template_name = 'crud/update_page.html'

class NewsDeleteView(OnlyLoggedSuperuser, DeleteView):
    model = News
    template_name = 'crud/delete_page.html'
    success_url = reverse_lazy('index_page')

class NewsCreateView(OnlyLoggedSuperuser, CreateView):
    model = News
    template_name = 'crud/create_page.html'
    fields = ['title', 'title_uz', 'title_ru', 'title_en',
              'slug', 'body', 'body_uz', 'body_ru', 'body_en',
              'image', 'category', 'status']
    def form_valid(self, form):
        self.model = form.save(commit=False)
        if not self.model.slug:
            self.model.slug=slugify(self.model.title)
        self.model.save()
        return super().form_valid(form)

@login_required
@user_passes_test(lambda u:u.is_superuser)
def admin_page_view(request):
    admin_user = User.objects.filter(is_superuser=True)

    context = {
        'admin_users': admin_user
    }
    return render(request,'user/admin_page.html',context)

class SearchResultList(ListView):
    model = News
    template_name = 'news/search_result.html'
    context_object_name = 'barcha_yangiliklar'

    def get_queryset(self):
        query = self.request.GET.get('q')
        return News.objects.filter(
            Q(title__icontains=query) | Q(body__icontains=query)
        )
