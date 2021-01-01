from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
# Create your views here.

from rest_framework import viewsets
from rest_framework.response import Response
# view 에서 만들어놓은 Serializer와 model 연결시켜준다.
from .serializers import BenefitsSerializer
from .models import Benefits
from rest_framework import permissions
from django.core import serializers
from django.views import View
from rest_framework import generics
#class BenefitsView(viewsets.ModelViewSet):

#myapp/benefits2
def Benefits2(request):
    benefits2 = Benefits.objects.all()
    benefits_list = list(benefits2.values())
    return JsonResponse(benefits_list,safe=False, json_dumps_params={'ensure_ascii':False})

#myapp/benefits
def BenefitsView(request):
    benefits = Benefits.objects.all()
    context = {'benefits':benefits}
    return render(request,'myapp/BenefitsView.html',context) #templates>myapp>~.html
#sale product test
from . import prod_test
def saleproduct(request):
    list1 = ["오츠카)데미소다\n피치250ml\n3개 2,400원\n1,200원\n데미소다\nDemiSoda\nDemisoda l\n데미소다\n"]

    list2 = list1[0].split("\n")
    list2 = list(filter(None,list2))
    products = prod_test.selectTest(list2)
    return JsonResponse(products,safe=False, json_dumps_params={'ensure_ascii':False})
    #context = {'products':products}
    #return render(request, 'myapp/SaleProduct.html',context)
    #return HttpResponse(products)
"""
class MembershipView(generics.RetrieveDestroyAPIView):
    queryset = Benefits.objects.all()
    serializer_class = BenefitsSerializer
    def get_queryset(self):
        return Benefits.objects.all()"""

"""def renderfile():
    return render_to('myapp/ImageUpload.html')"""

#using model form
from .forms import DocumentForm
def upload2(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('media')
    else:
        form = DocumentForm()
    return render(request, 'myapp/ImageUpload.html', {
        'form': form
    })


def find_prod_info(result_list):
    #
    # result_list는 인식하여 받아온 글자들의 리스트(배열)
    #
    # 상품 정보 비교를 위한 코드 작성
    #
    # 1) string으로 정보를 보내 줄 거면 string 하나로 만들면 되고
    # 2) list로 정보를 하나씩 보낼 때에는 어느 순서로 정보를 보낼지 결정하여야 한다
    return result_list


# def make_statement(list_dicts):
#     if list_dicts == []:
#         return "상품을 찾지 못했습니다"
#     statement = ''
#     for p in list_dicts:
#         statement += '상품명은 ' + p['prod_name'] + '이고 '
#         statement += '가격은 ' + str(p['prod_price']) + '원이며 '
#         statement += p['event_cd'] + ' 행사 중입니다'
#     return statement

def make_statement(info):
    (events, prices, pnames) = info

    if events == [] or prices == [] or pnames == []:
        return "상품을 찾지 못했습니다"
    statement = ''
    for e in events:
        statement += e + ' '
    statement += ' 행사 중입니다.'

    statement += ' 가격은 '
    for p in prices:
        statement += str(p[0]) + '개당' + str(p[1]) + '원 '
    statement += '입니다.'

    statement += ' 상품명은 '
    for n in pnames:
        statement += n + ' '
    statement += '입니다'

    return statement

from .forms import ImageForm, QRForm
from myapp.functions import handle_uploaded_file
from django.db import models
from myapp.models import Photo, Qrcode
import pymysql
from .product import selectTest
from .get_product_info import get_product_info
from .qrcode import qr_result


def qrview(request):
    m = Qrcode()
    if request.method == 'POST':
        form = QRForm(request.POST)
        if form.is_valid():
            m.title = form.cleaned_data['title']
            m.prod_name = form.cleaned_data['prod_name']
            m.save()

            qr_prod = qr_result(m.title,m.prod_name)
            return JsonResponse(qr_prod, safe=False, json_dumps_params={'ensure_ascii': False})

        if not form.is_valid():
            return HttpResponse("Form is invalid")
    else:
        form = QRForm(request.POST)
        return render(request, "myapp/QRcode.html", {'form': form})


#  2020-11-29

from .automl_vision import automl_vision

def imageupload(request):
    m = Photo()
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            m.title = form.cleaned_data['title']    #펀의점명 string 업로드
            m.image = form.cleaned_data['image']    #이미지 파일
            m.upload = form.cleaned_data['upload']  #업로드 되는 날짜와 시간
            m.save()
            filename = request.FILES['image']._name
            filepath = 'media/media/' + filename
            result_list = automl_vision(filepath)

            if len(result_list) == 0:
                return HttpResponse("None")
            else:
                product_list = selectTest(m.title, result_list)   # kma
                new_list = []
                for j in product_list:
                    if j not in new_list:
                        new_list.append(j)
                #return HttpResponse(result_list_str)     # hms
                return JsonResponse(new_list, safe=False, json_dumps_params={'ensure_ascii': False})   #kma
                #return render(request, 'myapp/SaleProduct.html', context)
            # return HttpResponse("File uploaded successfully")
        #else:
            #form = ImageForm(request.post)
        if not form.is_valid():
            return HttpResponse("Form is invalid")

    else:
        form = ImageForm(request.POST, request.FILES)
        return render(request, "myapp/PhotoUpload.html", {'form': form})

# def imageupload(request):
#     m = Photo()
#     if request.method == 'POST':
#         form = ImageForm(request.POST, request.FILES)
#         if form.is_valid():
#             m.title = form.cleaned_data['title']    #펀의점명 string 업로드
#             m.image = form.cleaned_data['image']    #이미지 파일
#             m.upload = form.cleaned_data['upload']  #업로드 되는 날짜와 시간
#             m.save()
#             filename = request.FILES['image']._name
#             # detect_crop_hints('media/media/' + filename)
#             # results = my_detect_text('media/media/' + "output-crop.jpg")
#             results = my_detect_text('media/media/' + filename)    # 이미지파일 media/media 에 저장된다.
#             # 이 이미지를 google vision api로 돌린다.
#             # print(results)
#             if len(results) == 0:
#                 return HttpResponse("None")
#             else:
#                 result_str = results[0].description
#                 # print(result_str)
#                 #result_list = google vision 받아온 배열로 나눔
#                 result_list = result_str.split('\n')   # str to list
#                 result_list = [e for e in result_list if e != '']
#                 #prod_info = find_prod_info(result_list)
#                 #result_list를 selectTest인자로 넣음(인자를 사전형식으로 전달받으려면 앞에  ** 넣어줘야)
#                 product_list = selectTest(m.title, result_list)   # orig
#                 #context = product_list
#                 #prod_info_str = make_statement(get_product_info(result_list))   # hms
#                 """
#                 try:
#                     product_list = selectTest(m.title, result_list)
#                     #products.append({'prod_name':'꼬북칩', 'prod_price':'2000', 'event_cd':'1+1'})
#                     #prod_info = make_statement(products)
#                 except TypeError:
#                     list_str = find_prod_info(result_list)
#                     prod_info = m.title + '::' + '::'.join(list_str)"""
#
#                 #print(product_list)
#                 #return HttpResponse(prod_info_str)     # hms
#                 return JsonResponse(product_list, safe=False, json_dumps_params={'ensure_ascii': False})   #orig
#                 #return render(request, 'myapp/SaleProduct.html', context)
#             # return HttpResponse("File uploaded successfully")
#         #else:
#             #form = ImageForm(request.post)
#         if not form.is_valid():
#             return HttpResponse("Form is invalid")
#
#     else:
#         form = ImageForm(request.POST, request.FILES)
#         return render(request, "myapp/PhotoUpload.html", {'form': form})


#def imageupload(request):
#     m = Photo()
#     if request.method == 'POST':
#         form = ImageForm(request.POST, request.FILES)
#         if form.is_valid():
#             m.title = form.cleaned_data['title']
#             m.image = form.cleaned_data['image']
#             m.upload = form.cleaned_data['upload']
#            m.save()
#             return HttpResponse("File uploaded successfuly")
#     else:
#        form = ImageForm(request.POST, request.FILES)
#        return render(request, "myapp/PhotoUpload.html",{'form':form})



#구글 비전 호출하면서 이미지 넘겨준다.
def my_detect_text(path):
    """Detects text in the file."""

    import os
    #os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "/home/ubuntu/django_project/myapp/project-201516-4bffd5af4ac2.json"
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r"/home/ubuntu/django_project/myapp/CVSProject-3f0fef841a96.json"
    import io

    # Imports the Google Cloud client library
    from google.cloud import vision

    # Instantiates a client 사용할 클라이언트 설정
    client = vision.ImageAnnotatorClient()

    # Loads the image into memory 이미지 읽기
    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.types.Image(content=content)

    # Performs label detection on the image file LABEL뽑아냄
    response = client.text_detection(image=image)
    texts = response.text_annotations

    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))

    return texts


#import cv2
#import io
#from matplotlib import pyplot as plt
#import numpy as np
# from google.cloud import vision
# from google.cloud.vision import types
#
# def detect_crop_hints(path):
#     """Detects crop hints in an image."""
#     import os
#     #os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "/home/ubuntu/django_project/myapp/project-201516-4bffd5af4ac2.json"
#     os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r"/home/ubuntu/django_project/myapp/CVSProject-3f0fef841a96.json"
#
#     from google.cloud import vision
#     import io
#     client = vision.ImageAnnotatorClient()
#
#     with io.open(path, 'rb') as image_file:
#         content = image_file.read()
#     image = vision.types.Image(content=content)
#
#     crop_hints_params = vision.types.CropHintsParams(aspect_ratios=[1.5])
#     # crop_hints_params = vision.types.CropHintsParams()
#     image_context = vision.types.ImageContext(
#         crop_hints_params=crop_hints_params)
#
#     response = client.crop_hints(image=image, image_context=image_context)
#     hints = response.crop_hints_annotation.crop_hints
#
#     img = cv2.imread(path)
#     orig = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
#     hint = hints[0]
#     pts = [(vertex.x, vertex.y) for vertex in hint.bounding_poly.vertices]
#     x, y = pts[0]
#     w = pts[1][0] - pts[0][0]
#     h = pts[3][1] - pts[0][1]
#     img = orig
#     crop_img = img[y:y + h, x:x + w]
#     cv2.imwrite('media/media/' + "output-crop.jpg", crop_img)
#
#     if response.error.message:
#         raise Exception(
#             '{}\nFor more info on error messages, check: '
#             'https://cloud.google.com/apis/design/errors'.format(
#                 response.error.message))
# client >서버주소/upload/로 파일을 넘기면
def upload(request):
    if request.method == 'POST':
        if 'file' in request.FILES:
            file = request.FILES['file']
            filename = file._name

            fp = open('%s/%s' % ('media/', filename), 'wb')
            for chunk in file.chunks():
                fp.write(chunk)
            fp.close()

            results = my_detect_text('media/' + filename)
            if len(results) == 0:
                return HttpResponse("None")
            else:
                return HttpResponse(results[0].description)
            #return HttpResponse('File Uploaded')
    else:
        return HttpResponse('Failed to Upload File')


# client >서버주소/upload/로 파일을 넘기면
# def upload(request):
#     if request.method == 'POST':
#         if 'file' in request.FILES:
#             file = request.FILES['file']
#             filename = file._name
#             fp = open('%s/%s' % ('media/',filename),'wb')
#             for chunk in file.chunks():
#                 fp.write(chunk)
#             fp.close()
#             return HttpResponse('File Uploaded')
#     return HttpResponse('Failed to Upload File!!!!')


""" # using FileSystemStorage
def upload(request):
    if request.method == 'POST':
        if 'file' in request.FILES:
            file = request.FILES['file']
            #filename = file._name
            fs = FileSystemStorage() #1
            filename = fs.save(file.name, file)#2
            uploaded_file_url = fs.url(filename) #3
            fp = open('%s/%s' % ('media/',filename),'wb')
            for chunk in file.chunks():
                fp.write(chunk)
            fp.close()
            return render(request,'myapp/ImageUpload.html', {
            'uploaded_file_url': uploaded_file_url})#4
            #return HttpResponse('File Uploaded')
    #return HttpResponse('Failed to Upload File')
    return render(request, 'myapp/ImageUpload.html') 
    """


