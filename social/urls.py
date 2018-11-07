"""social URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView
from django.conf import settings
#from account.views import register
from django.conf.urls.static import static
from navigation import views
from django.contrib.auth import views as auth_views
from navigation import views as nag_view

urlpatterns = [

    path('admin/', admin.site.urls),
    path('blog/', include('blog.urls', )),
    path('account/', include('account.urls')),
    path('image/', include('image.urls')),
    path('index/', views.index, name='index'),
    path('',auth_views.login,name='login'),
    path('contact/', nag_view.contact, name='contact'),
    #path('', TemplateView.as_view(template_name='account/dashboard.html'), name='dashboard'),
    #path('register/', register, name='register'),
    #path('registration_done/', TemplateView.as_view(template_name='account/register_done.html')),
    #path('logout/', TemplateView.as_view(template_name='account/logged_on.html'), name='logout'),
    #path('password_change/done/', TemplateView.as_view(template_name='account/password_change_done.html'),name='password_change_done'),
    #path('password_change/', TemplateView.as_view(template_name='account/password_change_form.html'),name='password_change'),
    #path('password_reset/complete/', TemplateView.as_view(template_name='account/password_reset_complete.html'),name='password_reset_complete'),
    #path('password_reset/confirm/', TemplateView.as_view(template_name='account/password_reset_confirm.html'),name='password_change_confirm'),
    #path('password_reset/done/', TemplateView.as_view(template_name='account/password_reset_done.html'),name='password_reset_done'),
    #path('password_reset/email/', TemplateView.as_view(template_name='account/password_reset_email.html'),name='password_reset_email'),
    #path('password_reset/', TemplateView.as_view(template_name='account/password_reset_form.html'),name="password_reset"),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)+ static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS)