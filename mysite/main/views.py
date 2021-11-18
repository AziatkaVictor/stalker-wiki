from django.shortcuts import render, redirect
from .models import Page, Type, Stalker, History, HistoryType
from .forms import CreateUserForm, CreateArticle
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Count
from datetime import datetime

# Create your views here.
def main_page(request):
    if request.method == 'GET':
        pages = Page.objects.order_by('-date_publish')[:5]
        count = len(Page.objects.all())
        context = {'pages' : pages, 'count' : count}
        return render(request, 'main/main.html', context)

def review(request):
    if request.method == 'GET':
        pages = Page.objects.order_by('name')
        types = Type.objects.order_by('id')
        stalkers = Stalker.objects.order_by('id')
        context = {'pages': pages, 'types': types, 'stalkers': stalkers}
        return render(request, 'main/review.html', context)

def registration_user(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('login')

        else:
            form = CreateUserForm()

        context = {'form' : form}
        return render(request, 'main/regist.html', context)

def login_user(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        error = ''
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                error = 'Логин или пароль неверны!'

        context = {'error': error}
        return render(request, 'main/login.html', context)


@login_required(login_url='login')
def logout_user(request):
    logout(request)
    return redirect('home')

@login_required(login_url='login')
def add_article(request):
    form = CreateArticle()

    if request.method == 'POST':
        form = CreateArticle(request.POST)
        if form.is_valid():
            article = form.save()
            article.author = request.user
            article.save()

            history = History()
            history.type = HistoryType.objects.get(name="Add")
            history.author = request.user
            history.info = Page.objects.get(pk=article.id)
            history.info_name = Page.objects.get(pk=article.id).name
            history.save()

            return redirect('article-detail', pk=article.id)

    context = {'form': form}
    return render(request, 'main/add_article.html', context)

def history_page(request):

    history = History.objects.order_by('-date')
    context = {'history': history}
    return render(request, 'main/history_page.html', context)

class ArticleDetailView(DetailView):
    model = Page

class ArticleEditView(UpdateView):

    model = Page
    fields = ['name', 'content', 'type', 'stalker']
    template_name_suffix = '_edit'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        history = History()
        history.type = HistoryType.objects.get(name="Edit")
        history.author = request.user
        history.info = Page.objects.get(pk=self.object.id)
        history.info_name = Page.objects.get(pk=self.object.id).name
        history.save()

        return super(ArticleEditView, self).post(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('home')
        else:
            self.object = self.get_object()
            return super().get(request, *args, **kwargs)

def info(request):
    if request.method == 'GET':
        pages = Page.objects.order_by('name')
        types = Type.objects.order_by('name')
        stalkers = Stalker.objects.order_by('id')
        users = User.objects.all().annotate(num_posts=Count('page')).order_by('-num_posts')
        context = {'pages': pages, 'types': types, 'stalkers': stalkers, 'users' : users}
        return render(request, 'main/info.html', context)
