"""exp1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin

urlpatterns = [
    url(r'^$', 'consult.views.home', name='home'),
    url(r'^([a-zA-Z]\w+)/affiliation/$', 'consult.views.affiliation', name='affiliation'),
    url(r'^([a-zA-Z]\w+)/application/$', 'consult.views.application', name='application'),
    url(r'^([a-zA-Z]\w+)/focalization/$', 'consult.views.focalization', name='focalization'),
    url(r'^([a-zA-Z]\w+)/comparison/$', 'consult.views.comparison', name='comparison'),
    url(r'^([a-zA-Z]\w+)/results/$', 'consult.views.results', name='results'),
    url(r'^contact/$', 'consult.views.contact', name='contact'),
    url(r'^about/$', 'consult.views.about', name='about'),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^success_close/$', 'consult.views.success_close', name='success_close'),
    url(r'^NewConsulteeAffiliation/$', 'consult.views.NewConsulteeAffiliation', name='NewConsulteeAffiliation'),
    url(r'^user_actions/$', 'consult.views.user_actions', name='user_actions'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
