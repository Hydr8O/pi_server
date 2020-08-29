from django.shortcuts import render
from .models import VisitorDetection
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile

def visitors(request):
    # image = Image.open('filefield-django-models-1.png')
    # image_io = BytesIO()
    # image.save(image_io, format='PNG')
    # VisitorDetection.objects.create(image=ContentFile(content=image_io.getvalue(), name='test_image'))
    image = VisitorDetection.objects.get(pk=2)
    return(render(
        request,
        'pi_visitors/visitors.html',
        {'image': image}
    ))
