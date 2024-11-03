from django import forms
from .models import ImageUpload

class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = ImageUpload
        fields = ['image']
from django import forms
from .models import ImageUpload

class ImageUploadForm(forms.ModelForm):
    quality = forms.IntegerField(min_value=1, max_value=100, initial=80, label="Compression Quality (1-100)", required=False)
    resize_percentage = forms.IntegerField(min_value=1, max_value=100, initial=100, label="Resize Percentage (1-100)", required=False)

    class Meta:
        model = ImageUpload
        fields = ['image', 'quality', 'resize_percentage']  # Include the resize_percentage field in the form
