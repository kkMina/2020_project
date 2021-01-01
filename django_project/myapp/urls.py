from django.urls import path, include
from . import views
from rest_framework.urlpatterns import format_suffix_patterns
from .views import BenefitsView, Benefits2
from .views import upload, upload2, imageupload,saleproduct,qrview

urlpatterns = format_suffix_patterns([
    path('auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('benefits/', views.BenefitsView, name='BenefitsView'),
    path('benefits2/', views.Benefits2, name='Benefits2'),
    path('upload2/', views.upload2, name='upload2'),
    path('upload/', views.upload, name='upload'),
    path('imageupload/', views.imageupload, name='imageupload'),
    path('product/', views.saleproduct, name='saleproduct'),
    path('qrview/', views.qrview, name='qrview'),
])

app_name='myapp'