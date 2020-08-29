from django.shortcuts import render
from .models import VisitorDetection
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile

def visitors(request):
    visitors = VisitorDetection.objects.all()
    return(render(
        request,
        'pi_visitors/visitors.html',
        {'visitors': visitors}
    ))
