from django.urls import path
from . import views

urlpatterns = [
    path('', views.main_page, name='home'),
    path('registration/', views.registration_user, name='regist'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('review/', views.review, name='review'),
    path('history/', views.history_page, name='history'),
    path('info/', views.info, name='info'),
    path('article/<int:pk>', views.ArticleDetailView.as_view(), name='article-detail'),
    path('article/edit/<int:pk>', views.ArticleEditView.as_view(), name='article-edit'),
    path('add_article/', views.add_article, name='add-article')
]