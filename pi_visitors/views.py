from django.shortcuts import render
from django.utils import timezone
from .models import VisitorDetection
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile

def visitors(request):
    if 'date' not in request.GET:
        visitors = VisitorDetection.objects.filter(detection_time__date=timezone.localdate())
    else:
        date = request.GET.get('date')
        visitors = VisitorDetection.objects.filter(detection_time__date=date)
    return(render(
        request,
        'pi_visitors/visitors.html',
        {'visitors': visitors}
    ))
    
def choose_date(request):
    return(render(
        request,
        'pi_visitors/choose_date.html'
    ))

# image = Image.open('sunset-picture.jpg')
    # image_io = BytesIO()
    # image.save(image_io, 'jpeg')
    # VisitorDetection.objects.create(image=ContentFile(image_io.getvalue(), name='test2.jpg'))