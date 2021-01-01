from rest_framework import serializers
from .models import Benefits
#from .models import Photo


class BenefitsSerializer(serializers.ModelSerializer):
    class Meta :
        model = Benefits
        fields = '__all__'
            #('id','conv_type','b_type', 'b_name','b_ex')
        #어떤 데이터 모델 / 필드 통신할지 설정
"""
class ImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(use_url=True)

    class Meta:
        model = Photo
        fields = ('post', 'image')"""