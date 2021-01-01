# -*- coding: utf-8 -*-

from django import forms
from .models import Post , Photo, Qrcode
class DocumentForm(forms.ModelForm):
    class Meta:
        model = Post
        fields =('title','image',)

    """
    views>def upload 마지막 부분return render(request, 'ImageUplaod.html', {'form': form})
    
    
    photoupload html
    <p><label for = "id_title">Title</label><input type="text" name="title" required id="id_title"></p>
        <p><label for = "id_uploaded">upload date</label><input type="text" name="upload" required id="id_uploaded"></p>
        <p><label for = "id_file">File:</label><input type="file" name="file" required id="id_file"></p>
            <button type="submit" class = "save btn btn-default">Upload</button>
    """
class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields= "__all__"
class ImageForm(forms.Form):
    title = forms.CharField()
    image = forms.ImageField()
    upload = forms.DateTimeField()

class QRForm(forms.Form):
    title = forms.CharField()
    prod_name = forms.CharField()
