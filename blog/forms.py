from django import forms
from .models import Post
from .models import Photo

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ('published_date', "user")





class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ('__all__')
