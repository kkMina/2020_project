"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.conf.urls import url
from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from django.views.static import serve
from django.conf import settings
from django.conf.urls import url

#################
from rest_framework import routers

urlpatterns = [
    path('admin/', admin.site.urls),
    path('myapp/', include('myapp.urls')), #Including another URLconf,
    path('shapp/', include('shapp.urls')),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

#DEBUG=TRUE, runserver 일때만 작동함.
#urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
"""
DEBUG=FALSE 인 경우에는 python manage.py runserver --insecure로 static file 까지는 제공가능하지만,
media의 경우 지원되지 않음. >>
urlpatterns+=url(r'^media/(?P<path>.\*)$', serve, {
    'document_root': settings.MEDIA_ROOT,
})
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

"""
